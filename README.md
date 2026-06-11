<p align="center">
  <img src="assets/banner.svg" alt="GeoRS-Pipeline" width="100%">
</p>

<h1 align="center">GeoRS-Pipeline 🛰️📄</h1>

<p align="center">
  <strong>全自动遥感研究流水线 — 从研究主题到完整论文，一键完成</strong><br>
  <em>Fully automated remote sensing research pipeline: topic in → paper out</em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-examples">Examples</a>
</p>

---

## ✨ Features

| 阶段 | 功能 |
|------|------|
| **文献调研** | 自动检索、提取、结构化文献信息，识别研究缺口 |
| **实验设计** | 从文献提炼 3-5 个可执行遥感任务，含数据源、模型、创新点 |
| **自动执行** | 基于 Google Earth Engine 全自动运行遥感分析任务 |
| **论文生成** | SCI 标准论文草稿，含图表、精度表、参考文献 |
| **一键输出** | 论文(md/docx) + 代码 + 数据 + 图表，打包输出 |

---

## 🚀 Quick Start

```powershell
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行全流水线
python scripts/run_pipeline.py `
    --topic "黄河流域植被覆盖度变化监测" `
    --project your-gee-project-id `
    --region "黄河中游" `
    --time "2018-2023"

# 3. 仅文献调研（不执行 GEE）
python scripts/run_pipeline.py --topic "..." --dry-run
```

---

## 📦 Installation

```powershell
git clone https://github.com/xingguangYan/GeoRS-Pipeline.git
cd GeoRS-Pipeline
pip install -r requirements.txt
```

### GEE 认证

```powershell
earthengine authenticate
```

### 环境验证

```powershell
python scripts/check_environment.py --project PROJECT_ID
```

---

## 🔬 How It Works

```mermaid
graph LR
    A[研究主题] --> B[ResearchX<br>文献检索]
    B --> C[研究缺口<br>任务提炼]
    C --> D[GEEPro<br>自动执行]
    D --> E[ResearchX<br>论文生成]
    E --> F[完整论文+代码+数据]
```

### Phase 1: 文献调研

自动检索 Google Scholar / Web of Science，提取 20-30 篇相关文献的结构化信息，识别 3-5 个研究缺口。

### Phase 2: GEE 任务执行

针对每个任务自动生成并执行 GEE Python 代码，支持 Sentinel-2、Landsat、MODIS 等多源数据。

### Phase 3: 论文生成

整合实验结果，按照 SCI 期刊标准生成完整论文草稿，含图表、精度表和参考文献。

---

## 📊 Examples

| 主题 | 任务数 | 输出 |
|------|--------|------|
| 湖泊富营养化监测 | 4 | 叶绿素反演图、时间序列、分类图 |
| 城市热岛效应 | 3 | LST 反演、趋势分析、土地利用分类 |
| 森林砍伐监测 | 5 | 森林损失图、驱动因素分析、预测模型 |

---

## 📁 Project Structure

```
GeoRS-Pipeline/
├── SKILL.md                  # Codex 技能指令
├── README.md                 # 本文件
├── requirements.txt          # Python 依赖
├── LICENSE                   # MIT 许可证
├── .gitignore
├── scripts/
│   ├── run_pipeline.py       # 主流程编排器
│   ├── literature_search.py  # 文献检索模块
│   ├── task_designer.py      # 任务设计模块
│   ├── paper_writer.py       # 论文生成模块
│   └── check_environment.py  # 环境检查
├── references/
│   ├── 01_workflow.md        # 详细工作流
│   └── 02_output_format.md   # 输出格式规范
└── templates/
    ├── manuscript_template.md # 论文模板
    └── task_template.json    # 任务模板
```

---

## 📄 License

MIT © xingguangYan
