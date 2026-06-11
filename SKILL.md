---
name: paperforge
description: |
  End-to-end automated remote sensing research pipeline. From a natural-language research topic to a complete SCI-grade manuscript with GEE-computed figures, tables, and code — fully automated.
  Combines ResearchX (literature mining/paper writing) and GEEPro (Earth Engine execution).
trigger_strategy: contains_any
trigger_terms:
  # English triggers
  - paperforge
  - paper forge
  - auto paper
  - research pipeline
  - remote sensing paper
  - GEE paper
  - automated research
  - write remote sensing paper
  - generate paper
  - paper automation
  - science paper
  - full pipeline
  - from topic to paper
  - paper writer
  - AI paper
  - research automation
  - literature to paper
  - topic to manuscript
  - auto manuscript
  - geospatial paper
  - earth engine paper
  - satellite paper
  - SCI paper
  - research pipeline automation
  - remote sensing manuscript
  # Chinese triggers
  - 论文锻造
  - 自动写论文
  - 遥感论文
  - 论文自动化
  - 全自动论文
  - 研究流水线
  - 课题到论文
  - 一键论文
  - 自动生成论文
  - 综合研究
  - GEE 论文
  - 遥感写作
  - 文献到论文
  - 论文生成器
  - 科研自动化
  - 论文助手
  - 学术写作
  - 研究助手
  # ResearchX triggers
  - research paper
  - SCI
  - journal paper
  - literature review
  - research gap
  - manuscript
  - write paper
  - experiment design
  - peer review
  - grant proposal
  - academic writing
  - publish paper
  - paper analysis
  - research topic
  - literature survey
  # GEEPro triggers
  - google earth engine
  - GEE
  - geemap
  - sentinel-2
  - landsat
  - MODIS
  - NDVI
  - remote sensing
  - earth engine
  # Platform discovery
  - paperforge skill
  - paperforge pipeline
  - install paperforge
  - skill paperforge
---

# 🔨 PaperForge — 全自动遥感科研流水线

> **"Topic in, Paper out."**

PaperForge 是一个端到端的智能研究流水线技能（Skill），集成了 **ResearchX**（文献挖掘、实验设计、论文写作）和 **GEEPro**（Google Earth Engine 代码执行）。你只需说出一个研究方向，PaperForge 就会自动完成：**文献检索 → 研究缺口分析 → GEE 实验设计 → 代码执行 → 结果分析 → SCI 标准论文生成**。

---

## 📋 目录

- [🔨 PaperForge — 全自动遥感科研流水线](#-paperforge--全自动遥感科研流水线)
  - [📋 目录](#-目录)
  - [✨ 核心能力一览](#-核心能力一览)
  - [⚡ 快速开始（30 秒上手）](#-快速开始-30-秒上手)
  - [🖥️ 在所有 Agent 平台中使用 PaperForge](#️-在所有-agent-平台中使用-paperforge)
    - [Cline (VS Code)](#cline-vs-code)
    - [Claude Desktop](#claude-desktop)
    - [Cursor](#cursor)
    - [Windsurf](#windsurf)
    - [GitHub Copilot](#github-copilot)
    - [OpenAI Codex CLI](#openai-codex-cli)
  - [🔬 完整工作流程详解](#-完整工作流程详解)
    - [Phase 1: ResearchX — 深度文献检索与任务提炼](#-phase-1-researchx--深度文献检索与任务提炼)
    - [Phase 2: GEEPro — 多任务自动执行](#-phase-2-geepro--多任务自动执行)
    - [Phase 3: ResearchX — 论文生成](#-phase-3-researchx--论文生成)
  - [📦 输入输出格式](#-输入输出格式)
    - [用户输入](#用户输入)
    - [最终输出](#最终输出)
  - [🎯 完整示例](#-完整示例)
    - [示例 1：黄河流域植被覆盖度变化](#示例-1黄河流域植被覆盖度变化)
    - [示例 2：湖泊富营养化监测](#示例-2湖泊富营养化监测)
  - [⚙️ 命令行参数](#️-命令行参数)
  - [📁 文件结构](#-文件结构)
  - [🛠️ 依赖与环境](#️-依赖与环境)
  - [❓ 常见问题](#-常见问题)
  - [📄 许可](#-许可)

---

## ✨ 核心能力一览

| # | 能力 | 说明 |
|---|------|------|
| 1 | **文献自动检索** | 多轮 web_search，提取 20-30 篇文献的结构化信息（数据源、算法、精度、创新点、局限） |
| 2 | **研究缺口分析** | 对比文献自动归纳 3-5 个尚未充分解决的方向 |
| 3 | **实验任务设计** | 将缺口转化为可执行的 GEE 任务（含数据源、模型、评估指标） |
| 4 | **GEE 代码自动生成** | 为每个任务生成完整的 Python GEE 脚本（RF/SVM/U-Net/LandTrendr 等） |
| 5 | **GEE 任务自动执行** | 在 GEE 上运行代码并导出结果（栅格、矢量、统计、图表） |
| 6 | **自动精度评估** | 计算 OA/Kappa/R²/RMSE 等指标，对比多算法性能 |
| 7 | **SCI 论文自动生成** | 按 SCI 期刊结构生成完整草稿，含摘要、引言、方法、结果、讨论、结论 |
| 8 | **自动图表插入** | 所有结果图自动嵌入论文，精度表自动生成 |
| 9 | **参考文献自动生成** | GB/T 7714-2025 / APA / MLA 格式，30 条文献 |
| 10 | **一键打包输出** | 论文 + 代码 + 数据 + 图表，结构化输出 |

---

## ⚡ 快速开始（30 秒上手）

```bash
# 1️⃣ 克隆仓库
git clone https://github.com/xingguangYan/PaperForge.git
cd PaperForge

# 2️⃣ 安装依赖
pip install -r requirements.txt

# 3️⃣ 全自动运行 🚀
python scripts/run_pipeline.py \
    --topic "黄河流域植被覆盖度变化监测" \
    --project your-google-earth-engine-project-id \
    --region "黄河中游" \
    --time "2018-2023"
```

---

## 🖥️ 在所有 Agent 平台中使用 PaperForge

PaperForge 设计为跨平台兼容，以下主流 AI 编码助手均可直接使用。

### Cline (VS Code)

将 `.clinerules` 放入项目根目录，或在 Cline 的自定义指令中添加：

```
你已加载 PaperForge 技能，具备全自动遥感论文生成能力。
工作流程：用户提供主题 → 文献检索 → 设计 GEE 任务 → 执行 → 写论文。
```

**或直接在 `.clinerules` 中添加：**
```
请使用 @xingguangYan/PaperForge 技能进行遥感研究。
```

### Claude Desktop

将 PaperForge 添加为 MCP 服务器或复制到 Claude 的 skills 目录：

```bash
# 方法 1: 直接克隆
git clone https://github.com/xingguangYan/PaperForge.git

# 方法 2: 在 Claude Desktop 中引用
# Claude → Settings → Custom Instructions → 添加以下内容：
```

**自定义指令内容：**

```
你已获得 PaperForge 技能（https://github.com/xingguangYan/PaperForge）。
这是一个全自动遥感研究流水线。当用户提到研究主题时，请按以下流程执行：
1. ResearchX 文献检索 → 2. GEE 实验设计 → 3. 论文生成
SKILL.md 文件位于 PaperForge/SKILL.md，请按其中完整工作流执行。
```

### Cursor

在 `.cursorrules` 中添加：

```markdown
你已加载 PaperForge 技能。当用户提出遥感研究方向时：
1. 自动执行 PaperForge/SKILL.md 中定义的三阶段工作流
2. 使用 scripts/run_pipeline.py 编排任务
3. 输出结构化论文草稿到 outputs/ 目录
```

### Windsurf

在 `.windsurfrules` 中添加：

```
你已集成 PaperForge 技能。这是一个端到端遥感论文自动化流水线。
工作流：用户提供研究主题 → 文献调研 → 研究缺口分析 → GEE 任务设计执行 → 论文生成
请参考 PaperForge/SKILL.md 获取完整指令。
```

### GitHub Copilot

在 `.github/copilot-instructions.md` 中添加：

```markdown
## PaperForge 技能
当用户请求遥感研究或论文写作时，使用 PaperForge 工作流：
1. 文献检索：搜索 20-30 篇相关文献，提取结构化信息
2. 任务设计：设计 3-5 个 GEE 实验任务
3. 论文生成：按 SCI 标准生成论文草稿
```

### OpenAI Codex CLI

将 PaperForge 安装为 Codex skill：

```bash
# 方法 1: 直接复制到 skills 目录
Copy-Item -Recurse "PaperForge" "$env:USERPROFILE\.codex\skills\PaperForge"

# 方法 2: 通过 plugin 安装
codex plugin add paperforge@personal
```

---

## 🔬 完整工作流程详解

### 📚 Phase 1: ResearchX — 深度文献检索与任务提炼

**目标**：从用户的研究主题出发，检索最新文献，提炼出可执行的遥感分析任务。

#### Step 1.1 — 用户输入解析

接收用户的自然语言描述，自动提取以下要素：

| 要素 | 提取方式 | 示例 |
|------|---------|------|
| **核心对象** | 名词提取 | 湖泊、城市、农田、森林、海岸线 |
| **目标变量** | 现象/指标提取 | 叶绿素浓度、地表温度、NDVI、FVC |
| **时间范围** | 数字+时间单位 | 2018-2023、近5年（默认）、2000-2020 |
| **空间范围** | 地名/坐标 | 黄河流域、长三角、陕西省 |
| **数据偏好** | 卫星名称 | Sentinel-2、Landsat-8/9、MODIS（无则自动推荐） |

**如果用户输入模糊**，主动追问：
```
研究区域是哪里？（例如：黄河流域、长三角、全球尺度）
时间范围是什么？（默认近5年）
是否有偏好的卫星数据？（推荐 Sentinel-2 或 Landsat）
```

#### Step 1.2 — 系统化文献检索

执行多轮 `web_search` 检索：

```
第一轮： [核心主题] + [遥感/GEE] + [近5年]
第二轮： [核心主题] + [具体方法] + [精度]
第三轮： [核心主题] + [研究缺口/挑战/未来方向]
```

**检索标准**：
- ✅ 最少检索 **15 篇以上** 高质量文献
- ✅ 最终引用 **25-30 条**（含中文核心期刊）
- ✅ 覆盖 3-5 种不同方法/模型
- ✅ 包含具体的精度数值（如 OA=0.92, R²=0.87）

#### Step 1.3 — 文献信息结构化提取

对每篇文献，提取以下信息并保存为结构化数据：

```json
{
  "title": "Monitoring vegetation dynamics...",
  "year": 2023,
  "journal": "Remote Sensing of Environment",
  "data_source": "Sentinel-2, Landsat-8",
  "preprocessing": ["cloud_masking", "atmospheric_correction"],
  "algorithm": "Random Forest",
  "accuracy": {"OA": 0.92, "Kappa": 0.89},
  "innovation": "提出了新的物候特征",
  "limitation": "仅适用于单一年份"
}
```

#### Step 1.4 — 研究缺口分析与任务提炼

基于文献对比分析，找出 **3-5 个** 研究缺口，每个缺口转化为一个具体的 GEE 任务：

| 属性 | 说明 | 示例值 |
|------|------|--------|
| **任务ID** | 唯一标识 | `Task-1` |
| **任务类型** | 分类/监测/回归/检测/时序 | `classification` |
| **目标变量** | 预测目标 | `land_cover_type` |
| **推荐数据源** | GEE 数据集名称 + 参数 | `COPERNICUS/S2_SR`, 云量<20% |
| **研究区域** | 具体边界 | 黄河中游（陕西-山西段） |
| **时间范围** | 起始-结束 | `2018-01-01` ~ `2023-12-31` |
| **基线模型** | 2-3 个文献常用方法 | `smileRandomForest`, `smileCart` |
| **改进模型/方法** | 本研究的创新方案 | 引入多时相纹理特征的 RF |
| **评估指标** | 精度评价标准 | `OA, Kappa, F1` 或 `R², RMSE` |
| **预期输出** | 产出的数据类型 | 分类图、面积统计、精度表 |
| **创新点** | 一句话说明改进 | 融合光学+SAR 多时序特征 |

#### Step 1.5 — 输出任务清单

保存为 `task_list.json`，供 Phase 2 使用。

---

### 🛰️ Phase 2: GEEPro — 多任务自动执行

**目标**：对 Phase 1 设计的每个任务，在 Google Earth Engine 上自动执行。

#### Step 2.1 — 环境验证

```python
# 验证 GEE 是否就绪
import ee
ee.Initialize(project="your-project-id")
print("GEE 环境就绪")
```

**如果认证失败**，提示用户：
```
请运行以下命令进行 GEE 认证：
    earthengine authenticate --quiet
或设置服务账号：
    ee.Initialize(project="your-project-id", credentials="service_account.json")
```

#### Step 2.2 — 任务执行流程

对每个任务，按以下步骤执行：

```
┌─────────────────────────────────────────────────────┐
│  ① 数据加载                                         │
│  ├─ ee.ImageCollection(dataset_id)                  │
│  ├─ .filterBounds(roi)                              │
│  ├─ .filterDate(start, end)                         │
│  └─ .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))  │
├─────────────────────────────────────────────────────┤
│  ② 预处理                                           │
│  ├─ 云掩膜 (QA60 / pixel_qa)                        │
│  ├─ 缩放 (multiply + add)                            │
│  └─ 裁剪到 ROI                                      │
├─────────────────────────────────────────────────────┤
│  ③ 特征工程                                         │
│  ├─ 光谱指数: NDVI, NDWI, EVI, NBR, mNDWI          │
│  ├─ 纹理特征: GLCM (contrast, correlation, entropy) │
│  └─ 时序特征: 减 - 加均值、斜率                        │
├─────────────────────────────────────────────────────┤
│  ④ 模型训练/推理                                    │
│  ├─ 分类: RandomForest / SVM / CART                 │
│  ├─ 回归: RandomForestRegressor / linearFit          │
│  ├─ 变化检测: LandTrendr / CCDC                     │
│  └─ 深度学习: U-Net / DeepLabV3+ (可选)             │
├─────────────────────────────────────────────────────┤
│  ⑤ 精度评估                                         │
│  ├─ 混淆矩阵 → OA, Kappa, PA, UA                    │
│  ├─ 回归 → R², RMSE, MAE, Bias                     │
│  └─ 变化检测 → 漏检率, 虚警率, F1                   │
├─────────────────────────────────────────────────────┤
│  ⑥ 结果导出                                         │
│  ├─ 栅格 → GeoTIFF (export.image.toDrive)           │
│  ├─ 矢量 → Shapefile (export.table.toDrive)          │
│  ├─ 统计 → CSV (ee.data.computePixels)               │
│  └─ 图表 → PNG (matplotlib 可视化)                   │
└─────────────────────────────────────────────────────┘
```

#### Step 2.3 — 自动降级策略

当遇到问题时，自动降级而非报错退出：

| 问题 | 检测条件 | 处理方式 |
|------|---------|---------|
| 数据集不可用 | API 返回 404/空 | 自动切换替代数据集（S2→L8→MODIS） |
| 内存超限 | "User memory limit exceeded" | 增大 scale 20% + 缩小 ROI |
| ROI 无有效像素 | "no valid pixels" | 自动扩大 ROI 或调整日期 |
| 认证过期 | "Authentication failed" | 提示重新认证，给出命令 |
| 网络超时 | 请求 > 30s | 重试 3 次，指数退避 |
| 代理限制 | 连接被拒绝 | 检测 HTTP_PROXY 设置并提示 |

#### Step 2.4 — 输出结构

```
runs/YYYYMMDD_HHMMSS_topic/
├── summary.json              # 所有任务汇总
├── Task-1/
│   ├── code.py               # 完整 GEE Python 脚本
│   ├── RUN.md                # 运行说明
│   ├── inputs.json           # 输入参数
│   ├── result.tif            # 输出栅格
│   ├── accuracy.json         # 精度评估
│   ├── statistics.csv        # 统计结果
│   └── figure.png            # 可视化结果图
├── Task-2/
│   └── ...
└── Task-3/
    └── ...
```

---

### 📝 Phase 3: ResearchX — 论文生成

**目标**：整合所有实验结果，生成符合 SCI 期刊标准的完整论文草稿。

#### Step 3.1 — 自动结果分析

- 读取所有任务的 `accuracy.json` 和 `statistics.csv`
- 生成多任务对比表格
- 提取关键数值（最高精度、变化面积、趋势斜率等）

#### Step 3.2 — 论文结构

论文按以下标准 SCI 结构生成：

**标题**：自动生成，格式为 `[方法]在[研究对象]的[目标变量][时间范围]研究`

**摘要**（200-300 字）：
```
背景（1句）+ 目的（1句）+ 方法（2-3句）+ 关键结果（3-5个数值）+ 意义（1句）
```

**引言**（5 段结构）：
```
第1段：大背景（遥感/环境/气候意义）
第2段：国内外研究进展（引用文献，对比各方法的优缺点）
第3段：现有不足（指出现有研究 gap）
第4段：本研究目标与创新点（列出 3-5 个任务及其科学假设）
第5段：文章结构安排
```

**方法**：
```
2.1 研究区概况（位置图、气候、地貌特征）
2.2 数据源（表格形式：卫星、传感器、波段、分辨率、时间、预处理）
2.3 任务一方法（包括公式、关键代码段、流程图）
2.4 任务二方法
...
2.N 精度评估方法（交叉验证、独立验证集）
```

**结果与分析**：
```
3.1 任务一结果（分类图/趋势图 + 精度表 + 统计分析）
3.2 任务二结果
...
3.N 综合分析（多任务交叉对比）
```

**讨论**：
```
4.1 与已有研究的对比（为什么一致/不一致）
4.2 方法局限性（数据、模型、样本等方面）
4.3 对实际应用的启示（政策建议、管理措施）
4.4 未来工作展望
```

**结论**（3-5 个要点）：
```
(1) ...
(2) ...
(3) ...
```

**参考文献**（25-30 条）：
- 格式：默认 GB/T 7714-2025
- 至少 20 条来自 Phase 1 检索的真实文献
- 其余为领域经典文献或补充

#### Step 3.3 — 自动图表生成

| 图表类型 | 格式 | 引用方式 |
|---------|------|---------|
| 研究区位置图 | PNG, 300 DPI | ![Fig 1](path) |
| 分类/结果图 | PNG, 300 DPI | ![Fig 2](path) |
| 变化趋势图 | PNG, 300 DPI | ![Fig 3](path) |
| 精度对比表 | Markdown/CSV | 表 1 |
| 面积统计表 | Markdown/CSV | 表 2 |
| 精度评估表 | Markdown/CSV | 表 3 |

#### Step 3.4 — 最终输出

```
outputs/YYYYMMDD_HHMMSS_topic/
├── manuscript.md             # 完整论文草稿（可转为 docx）
├── figures/                  # 所有结果图 (300 DPI PNG)
│   ├── fig1_study_area.png
│   ├── fig2_task1_result.png
│   └── ...
├── tables/                   # 精度表/统计表
│   ├── table1_accuracy.csv
│   ├── table1_accuracy.md
│   └── ...
├── gee_code/                 # 完整 GEE 脚本
│   ├── task1_code.py
│   └── ...
├── results_raw/              # 原始数据
│   ├── task1_result.tif
│   └── ...
└── README.md                 # 复现说明
```

---

## 📦 输入输出格式

### 用户输入

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| 研究主题 | 自然语言 | ✅ | - | 描述研究方向 |
| GEE Project ID | 字符串 | ⚠️ | 无 | 仅 Phase 2 需要 |
| 研究区域 | 字符串 | ❌ | 自动选择 | 地名或坐标 |
| 时间范围 | 字符串 | ❌ | 近5年 | 如 "2018-2023" |
| 任务数量 | 整数 | ❌ | 4 | 3-5 个 |
| 参考文献格式 | 字符串 | ❌ | gb | gb/apa/mla |
| 禁用深度学习 | 布尔 | ❌ | false | --no-deep |

### 最终输出

```
📦 outputs/YYYYMMDD_HHMMSS_topic/
├── 📄 manuscript.md          # 完整论文
├── 🖼️ figures/               # 图表
├── 📊 tables/                # 数据表
├── 💻 gee_code/              # 代码
└── 📁 results_raw/           # 原始结果
```

---

## 🎯 完整示例

### 示例 1：黄河流域植被覆盖度变化

**用户输入：**
> 研究方向：黄河流域植被覆盖度变化监测，时间范围 2018-2023。区域：黄河中游（陕西-山西段）。优先使用 Sentinel-2 数据，若云量过多则用 Landsat-8。

**PaperForge 自动执行流程：**

```
[Phase 1] ResearchX 文献检索...
  → 检索到 35 篇相关文献
  → 提取结构化信息（数据源、算法、精度）
  → 识别 4 个研究缺口

[Phase 2] GEEPro 自动执行...
  ✓ Task-1: FVC 回归估算（RF + Sentinel-2）→ R²=0.89
  ✓ Task-2: 植被趋势监测（LandTrendr）→ 12% 区域显著下降
  ✓ Task-3: 土地利用分类（S2 + L8）→ OA=0.93, Kappa=0.91
  ✓ Task-4: 退耕还林效果评估 → 森林面积增加 345 km²

[Phase 3] 论文生成...
  ✓ 摘要（256 字）
  ✓ 引言（5 段，15 条引用）
  ✓ 方法（4 个子节，含 GEE 代码段）
  ✓ 结果（4 张图 + 3 个表）
  ✓ 讨论（4 个方面）
  ✓ 结论（4 个要点）
  ✓ 参考文献（28 条，GB/T 7714-2025 格式）

✅ 完成！输出到 outputs/20260611_143022/
```

### 示例 2：湖泊富营养化监测

**用户输入：**
> 太湖富营养化遥感监测，使用 Sentinel-2 和 Landsat-8 数据，评估 2019-2023 年叶绿素 a 浓度变化。

**PaperForge 自动执行流程：**

```
[Phase 1] ResearchX 文献检索...
  → 检索到 28 篇关于湖泊富营养化遥感的文献
  → 提取常用算法：OC3、APD、机器学习回归
  → 设计 3 个任务

[Phase 2] GEEPro 自动执行...
  ✓ Task-1: 叶绿素 a 反演（OC3 算法 + S2）→ R²=0.85
  ✓ Task-2: 叶绿素 a 反演（随机森林 + S2+L8）→ R²=0.91
  ✓ Task-3: 富营养化时序趋势分析 → Eutrophic 指数下降 8%

[Phase 3] 论文生成...
  ✓ 论文草稿（含太湖位置图、Chl-a 反演图、趋势图）
  ✓ 25 条参考文献
  ✓ 完整 GEE 代码

✅ 完成！
```

---

## ⚙️ 命令行参数

```bash
python scripts/run_pipeline.py --topic "研究主题" [选项]
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `--topic` | **必填**。研究主题 | `"黄河流域植被覆盖度变化"` |
| `--project` | GEE Project ID | `"ee-myproject"` |
| `--region` | 研究区域 | `"黄河中游"`, `"35.5,110.2"` |
| `--time` | 时间范围（默认近5年） | `"2018-2023"` |
| `--tasks` | 任务数量 3-5（默认4） | `5` |
| `--format` | 参考文献格式 | `gb`（默认）, `apa`, `mla` |
| `--no-deep` | 禁用深度学习方法 | 无需值 |
| `--dry-run` | 仅出方案，不执行 GEE | 无需值 |
| `--phase` | 仅运行指定阶段 | `literature`, `gee`, `paper` |
| `--help` | 显示帮助 | 无需值 |

**使用示例：**
```bash
# 全自动运行
python scripts/run_pipeline.py --topic "城市热岛效应" --project my-project

# 仅文献调研 + 论文（跳过 GEE 执行）
python scripts/run_pipeline.py --topic "..." --dry-run

# 指定 APA 格式 + 5 个任务
python scripts/run_pipeline.py --topic "..." --project my-project --tasks 5 --format apa

# 仅执行 GEE 任务（跳过文献和论文）
python scripts/run_pipeline.py --topic "..." --project my-project --phase gee
```

---

## 📁 文件结构

```
PaperForge/
│
├── SKILL.md                     # 🔵 本文件 — 技能指令（入口）
├── README.md                    # GitHub 首页
├── requirements.txt             # Python 依赖
├── LICENSE                      # MIT 许可证
├── .gitignore
│
├── assets/
│   └── banner.svg               # 项目横幅
│
├── scripts/
│   ├── run_pipeline.py          # 🔵 主流水线编排器
│   └── check_environment.py     # GEE 环境检查
│
├── references/
│   ├── 01_workflow.md           # 详细工作流说明
│   └── 02_output_format.md      # 输出格式规范
│
└── templates/
    ├── manuscript_template.md    # SCI 论文模板
    └── task_template.json        # 任务 JSON 模板
```

---

## 🛠️ 依赖与环境

```bash
# 安装依赖
pip install -r requirements.txt
```

requirements.txt 内容：
```
earthengine-api>=1.0.0
geemap>=0.30.0
geopandas>=0.14.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
requests>=2.28.0
```

```bash
# GEE 认证
earthengine authenticate

# 环境验证
python scripts/check_environment.py --project PROJECT_ID
```

**代理设置（中国大陆用户）：**
```bash
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
```

---

## ❓ 常见问题

| 问题 | 解决方案 |
|------|---------|
| **GEE 认证失败** | `earthengine authenticate` 或使用服务账号 JSON |
| **调用 GEE 时网络超时** | 设置 HTTP_PROXY 环境变量（中国大陆用户） |
| **提示内存不足** | 增大 scale 值，或缩小研究区域 |
| **Python 报错 no module** | `pip install -r requirements.txt` |
| **找不到数据集** | 自动切换替代数据集，或检查数据集 ID |
| **文献检索结果太少** | PaperForge 会自动扩展关键词和同义词 |
| **想换参考文献格式** | 添加 `--format apa` 或 `--format mla` |
| **只想看方案不运行** | 添加 `--dry-run` |
| **论文想转 Word** | 使用 pandoc: `pandoc manuscript.md -o manuscript.docx` |

---

## 📄 许可

MIT License © 2026 [xingguangYan](https://github.com/xingguangYan)
