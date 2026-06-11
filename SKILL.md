---
name: geors-pipeline
description: |
  Fully automated remote sensing research pipeline integrating ResearchX (literature mining, experiment design, paper writing) and GEEPro (Google Earth Engine task execution).
  From a natural-language research topic to a complete manuscript with figures, tables, and code — fully automated.
  Covers: literature review, research gap identification, GEE task design & execution, result analysis, SCI-grade paper generation.
trigger_strategy: contains_any
trigger_terms:
  - geors pipeline
  - 综合研究
  - 全自动研究
  - 遥感论文
  - remote sensing paper
  - 遥感自动化
  - GEE 论文
  - GEE paper
  - 遥感科研
  - 论文自动化
  - 研究流水线
  - remote sensing research
  - automated research
  - 文献+GEE
  - full pipeline
  - 遥感综合
  - GEE research
---

# GeoRS-Pipeline — 全自动遥感研究流水线

GeoRS-Pipeline 是一个集成了 ResearchX（文献挖掘、实验设计、论文写作）与 GEEPro（Google Earth Engine 代码执行）的端到端智能研究助手。用户只需提供研究主题，即可自动完成从文献调研到完整论文生成的全流程。

## 工作流程总览

Phase 1: ResearchX 文献调研 → 任务提炼
Phase 2: GEEPro 多任务自动执行
Phase 3: ResearchX 结果整合 → 论文生成

## Phase 1: ResearchX — 深度文献检索与任务提炼

### 1.1 用户输入解析

接收用户自然语言研究主题，自动提取：
- 核心对象（湖泊、城市、农田、森林等）
- 变量/现象（叶绿素浓度、地表温度、土地利用变化等）
- 时间范围（默认近5年）
- 空间范围（默认中国典型区域或全球代表性区域）
- 数据偏好（Landsat、Sentinel、MODIS 等，无则自动推荐）

### 1.2 系统化文献检索

使用 web_search 进行多轮检索：
1. 关键词扩展：从主题生成同义词、上下位词
2. 检索数据库：Google Scholar, Web of Science（模拟）
3. 筛选标准：近5年、高质量期刊、含遥感/GEE 应用
4. 最少 10 篇高质量文献（最终引用 20-30 条）

### 1.3 文献信息提取

对每篇文献提取：
- 标题、作者、年份、期刊
- 数据源：卫星/传感器、波段组合、时间分辨率
- 预处理方法：云掩膜、大气校正等
- 模型/算法：RF、SVM、U-Net、LSTM、LandTrendr 等
- 评估指标：OA、Kappa、R²、RMSE 等
- 创新点与局限性
- 结果数值

### 1.4 研究缺口识别与任务提炼

归纳 3-5 个可执行遥感任务，每个任务包含：

| 属性 | 说明 |
|------|------|
| 任务ID | Task-1, Task-2 ... |
| 任务类型 | 分类/监测/回归/检测/时序 |
| 目标变量 | NDVI趋势、土地利用类别等 |
| 推荐数据源 | GEE数据集名称 |
| 区域建议 | GEE边界 |
| 参考模型 | 2-3基线+1改进 |
| 预期输出 | 分类图、变化栅格等 |
| 创新点 | 改进假设 |

### 1.5 输出 task_list.json

任务列表保存为 task_list.json，包含每个任务的完整定义。

## Phase 2: GEEPro — 多任务自动执行

### 2.1 环境准备

验证 GEE 环境：
python scripts/check_environment.py --project PROJECT_ID

### 2.2 任务执行流程

每个任务执行：
1. 数据加载：从 GEE 加载指定数据集
2. 预处理：云掩膜、裁剪、缩放
3. 特征工程：计算指数（NDVI、NDWI、EVI 等）、纹理特征
4. 模型训练/推理
5. 精度评估
6. 结果导出到本地
7. 记录运行日志

### 2.3 任务执行约束

- 单任务最大执行时间：20 分钟
- 总体流水线：不超过 2 小时（可配置）
- 并发：最多 3 个任务
- 结果缓存：同一主题重复运行返回缓存

### 2.4 自动降级策略

- 数据不可用 → 自动替换替代数据集
- 内存超限 → 缩小区域或增大 scale
- 认证失败 → 提示认证
- 网络错误 → 检测代理设置

### 2.5 输出结构

runs/YYYYMMDD_HHMMSS_topic/
  Task-1/code.py, RUN.md, result.tif, statistics.csv, accuracy.json, figure.png
  Task-2/...
  summary.json

## Phase 3: ResearchX — 论文生成

### 3.1 自动结果分析

读取所有任务输出，生成对比分析表格，提取关键数值。

### 3.2 标准论文结构

- 标题（自动生成）
- 作者（可配置）
- 摘要（200-300字）
- 引言（5段式）
- 方法（数据源表、研究区、流程、实验设置）
- 实验与结果（结果图、精度表、统计表）
- 讨论（可靠性、局限性、应用启示、未来工作）
- 结论（主要发现+贡献）
- 参考文献（GB/T 7714-2025，30条）

### 3.3 自动图表生成

所有结果图 PNG（300 DPI），精度表 Markdown/CSV。

### 3.4 输出文件

outputs/YYYYMMDD_HHMMSS_topic/
  manuscript.md, figures/, tables/, gee_code/, results_raw/, README.md

## 完整流程示例

用户：黄河流域植被覆盖度变化监测，2018-2023，黄河中游

1. 文献检索 → 35篇文献，4个任务
2. GEE执行：
   - Task1: FVC回归(RF+S2) → R²=0.89
   - Task2: 趋势监测(LandTrendr) → 12%下降
   - Task3: 土地利用分类 → OA=0.93
   - Task4: 退耕还林评估 → 森林+345km²
3. 论文生成 → 28条参考文献

## 命令行接口

python scripts/run_pipeline.py --topic "研究主题" --project PROJECT_ID
python scripts/run_pipeline.py --topic "..." --dry-run
python scripts/run_pipeline.py --topic "..." --phase literature|gee|paper

参数：--topic, --project, --region, --time, --tasks, --format, --no-deep, --dry-run

## 质量门禁

- 文献支撑：每个方法引用真实文献
- 量化结果：每个结果含具体数值
- 可复现：方法足够详细
- 批判性：至少讨论一个局限性
- 存档：保存到 outputs/ 目录

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| GEE未认证 | 提示 earthengine authenticate |
| 数据集不可用 | 自动切换替代 |
| 内存不足 | 自动降级 |
| 网络受限 | 参考代理设置 |
| 输入模糊 | 主动追问 |

## 依赖安装

pip install -r requirements.txt
