# PaperForge 详细工作流 (Workflow Reference)

> Referenced by `SKILL.md` §Phases. Load only when the corresponding phase
> needs detail. Version: 2.0.

## 三阶段总览 (Phase Overview)

```
用户输入研究方向 (user topic)
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Phase 1: ResearchX — 文献检索与任务提炼              │
│  Step 1: 用户输入解析                                │
│  Step 2: 多轮 web_search 文献检索 (3 rounds)        │
│  Step 3: 文献信息结构化提取                          │
│  Step 4: 研究缺口 → 3-5 个 GEE 任务                 │
│  Step 5: 输出 tasks/task_list.json                  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│ Phase 2: GEEPro — 多任务自动执行                     │
│  Step 1: 环境验证 (check_environment.py / ee.Initialize) │
│  Step 2: 数据加载 & 预处理 (gee_tasks.masked_sentinel2) │
│  Step 3: 逐年中值合成 + GeoTIFF 下载 (all years)    │
│  Step 4: 统计计算 (roi_stats / linear_trend / MK)   │
│  Step 5: 图表生成 (render_figures, 300 DPI)         │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│ Phase 3: ResearchX — 论文生成                       │
│  Step 1: 结果整合 & 多任务对比                       │
│  Step 2: 论文草稿 (摘要→引言→方法→结果→讨论→结论)    │
│  Step 3: paper_writer.write_outputs → md/html/docx  │
│  Step 4: 参考文献 (25-30条) 格式校验                │
└──────────────────────┬──────────────────────────────┘
                       ▼
              outputs/ 完整论文包
```

## 参数传递 (Data flow)

- Phase 1 输出: `tasks/task_list.json` → Phase 2 读取
- Phase 2 输出: `runs/YYYYMMDD_HHMMSS_topic/` → Phase 3 读取
- Phase 3 输出: `outputs/YYYYMMDD_HHMMSS_topic/` → 最终交付

## Phase 1 细节

### 输入解析 (Input parsing)

| 要素 | 提取方法 | 示例 |
|------|---------|------|
| Core Object | 名词短语 | Yellow River Basin, Taihu Lake |
| Target Variable | 指标提取 | vegetation cover, chl-a, LST |
| Time Range | 数字+时间单位 | 2018-2023 | 
| Spatial Range | 地名/坐标 | Wuhan, 35.5N/110.2E |
| Data Preference | 卫星名匹配 | Sentinel-2, Landsat, MODIS |

信息不足时必须提问: 研究区? 时间范围? 卫星偏好? 期刊类型?

### 文献检索三回合

```
Round 1 (Broad):   [topic] + remote sensing + [area]
Round 2 (Method):  [topic] + [RF/U-Net/LandTrendr]
Round 3 (Gap):     [topic] + limitations/challenges/future
```

质量标准: ≥15 篇, 最终 25-30 条引用, ≥3 种方法, 含精度数值 (OA/R²/Kappa/RMSE)。

### 结构化提取 schema

见 `templates/task_template.json`。每条记录: title, year, journal, data_source,
algorithm, accuracy, innovation, limitation。用 `scripts/literature.py`:
`validate_corpus(papers)` 检验是否达标。

### 研究缺口 → 任务

将 3-5 个缺口转换为 GEE 任务, 用 `scripts/gee_tasks.py:build_task(task_id,
task_type)` 生成 scaffold, 或手写后保存 `tasks/task_list.json`。

## Phase 2 细节

所有 GEE 操作优先复用 `scripts/gee_tasks.py` 中的幂等函数 (见 SKILL.md 表格)。
关键步骤:

1. `initialize(project=...)` — 认证失败则打印 `earthengine authenticate` 并降级 dry-run。
2. `masked_sentinel2(roi, start, end)` 加载并做 SCL 云掩膜 + NDVI/FVC/NDWI。
3. 逐年 `annual_median(col, year, "NDVI")`, 对每年每区 `download_tif(...)` 到
   `figures/ndvi_tif/` (硬性要求: 全部年份下载)。
4. `roi_stats` + `linear_trend` 计算统计量。
5. `render_figures.py` 生成 6 幅 300 DPI 图 (英文标签, 避免中文字体问题)。

## Phase 3 细节 (Manuscript)

结构字数要求见 `SKILL.md` §Phase 3 表格。公式 (行内 LaTeX 风格):

```
FVC   = (NDVI - NDVI_soil) / (NDVI_veg - NDVI_soil)
y     = β0 + β1·t + ε
S     = Σ_{i=1}^{n-1} Σ_{j=i+1}^{n} sgn(x_j - x_i)
OA    = (TP + TN) / (TP + TN + FP + FN)
Kappa = (p_o - p_e) / (1 - p_e)
```

图片引用格式:

```markdown
![Fig 2](figures/fig2_ndvi_timeseries.png)
*Fig 2 Annual mean NDVI variation for both study sites (2020-2025)*
```

导出必须调用 `scripts/paper_writer.py:write_outputs(results, out_dir)`,
生成 md + html + docx + `manuscript_stats.json`。

## 自动降级策略 (Degradation)

| 阶段 | 问题 | 降级方案 |
|------|------|---------|
| Phase 1 | web_search 0 结果 | 简化关键词, 中英双语, 同义词 |
| Phase 2 | GEE 未认证 | 提示认证命令, dry-run 模拟 |
| Phase 2 | 数据集不可用 | S2 → Landsat 8/9 → MODIS (`collection_with_fallback`) |
| Phase 2 | 内存超限 | 增大 scale, 缩小 ROI, bestEffort |
| Phase 2 | 网络超时 | 3 次重试指数退避 (`download_tif` 内置) |
| Phase 3 | 结果不足 | 用文献典型值标记 simulated |

## 平台接入 (Platform)

### OpenAI Codex CLI

```bash
python scripts/package_codex.py --target ~/.codex/skills
# 重启后输入: $paperforge
```

### Claude Code

```bash
cp -r PaperForge ~/.claude/skills/PaperForge   # 或 .claude/skills/PaperForge
```

### Cline / Cursor / Windsurf / Copilot

在对应 rules 文件 (`.clinerules` / `.cursorrules` / `.windsurfrules` /
`.github/copilot-instructions.md`) 加入:

```text
PaperForge skill loaded. For remote sensing research, run the 3-phase pipeline:
1. literature mining → task design → 2. GEE execution + TIF download +
figures → 3. 8000+ word manuscript (MD+HTML+DOCX). Always ask journal type
(Chinese Core / SCI), study area, time range, data preference first.
```
