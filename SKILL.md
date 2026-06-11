---
name: paperforge
description: |
  Professional-grade automated remote sensing research pipeline. From a natural-language topic to a complete SCI or Chinese-core journal manuscript (8000+ words) with GEE-computed figures, tables, formulas, and DOCX output — fully automated.
  Integrates ResearchX (literature mining/paper writing) and GEEPro (Earth Engine execution).
trigger_strategy: contains_any
trigger_terms:
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
  - 中文核心
  - SCI 写作
  - research paper
  - SCI
  - journal paper
  - literature review
  - research gap
  - manuscript
  - write paper
  - experiment design
  - peer review
  - academic writing
  - publish paper
  - google earth engine
  - GEE
  - geemap
  - sentinel-2
  - landsat
  - MODIS
  - NDVI
  - remote sensing
  - earth engine
---

# PaperForge — Professional Automated Remote Sensing Research Pipeline

> **"Topic in. Paper out."**

PaperForge is a production-grade Codex skill for end-to-end remote sensing research automation. It integrates **ResearchX** (literature mining, experiment design, paper writing) and **GEEPro** (Google Earth Engine code execution). Given a research topic, PaperForge autonomously completes: **literature review → research gap analysis → GEE task design → code execution → result analysis → complete manuscript generation (8000+ words) → DOCX output**.

---

## 0. Pre-Execution: Journal Type Selection

**BEFORE starting any task, ALWAYS ask the user:**

> "请问您要撰写的是以下哪种期刊类型？"
> 
> **① 中文核心期刊 (Chinese Core Journal)**
> - 约 6000-8000 字
> - 中英文摘要 + 关键词
> - GB/T 7714-2015 参考文献格式
> - 适合：《遥感学报》《生态学报》《地理学报》等
> 
> **② SCI 期刊 (SCI/SCIE Journal)**
> - 约 8000-10000 字
> - 英文长摘要 + Graphical Abstract
> - APA/MLA 参考文献格式
> - 适合：Remote Sensing of Environment, IEEE TGRS, Science of Remote Sensing 等

**Also ask about:**
- Study area boundaries (if not specified)
- Time range (default: last 5 years)
- Satellite data preference (Sentinel-2, Landsat, MODIS — auto-recommend if not specified)

---

## 1. Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PaperForge Automated Pipeline                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1: ResearchX — Deep Literature Mining & Task Design                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 1: Parse user input (study area, time, data preference)        │   │
│  │ Step 2: Multi-round web_search (3 rounds × 5+ queries)              │   │
│  │ Step 3: Structured literature extraction (15+ papers)               │   │
│  │ Step 4: Research gap identification → 3-5 GEE tasks                 │   │
│  │ Step 5: Output task_list.json                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                       │
│  Phase 2: GEEPro — Multi-Task Execution                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 1: Environment verification                                    │   │
│  │ Step 2: Download NDVI/FVC GeoTIFFs (all years, both areas)          │   │
│  │ Step 3: Compute accuracy & statistics                               │   │
│  │ Step 4: Generate publication-quality figures (PNG, 300 DPI)         │   │
│  │ Step 5: Save results to runs/ directory                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                       │
│  Phase 3: ResearchX — Complete Manuscript Generation                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 1: Integrate all results (tables, figures, statistics)         │   │
│  │ Step 2: Generate 8000+ word manuscript with:                        │   │
│  │   • Detailed introduction (1000+ words, 5 paragraphs)               │   │
│  │   • Methods with mathematical formulas and GEE code snippets        │   │
│  │   • Results with embedded figures and formatted tables              │   │
│  │   • Discussion and conclusion                                      │   │
│  │   • 25-30 formatted references                                      │   │
│  │ Step 3: Save as manuscript.md + manuscript.html + manuscript.docx   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Output: manuscript.md (8000+ words) + figures/ + tables/          │   │
│  │          + gee_code/ + ndvi_tif/ + manuscript.docx                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘


---

## Phase 1: ResearchX — Deep Literature Mining & Task Design

### 1.1 User Input Parsing

Extract from the user's natural language description:

| Element | Extraction Method | Example |
|---------|------------------|---------|
| **Core Object** | Noun phrase extraction | Yellow River Basin, Taihu Lake, Guishan Mountain |
| **Target Variable** | Indicator extraction | Vegetation cover, chlorophyll-a, LST, NDVI |
| **Time Range** | Number + time unit | 2018-2023, 2020-2025, last 5 years |
| **Spatial Range** | Place name / coordinates | Wuhan, 35.5N/110.2E, buffer 500m |
| **Data Preference** | Satellite name matching | Sentinel-2, Landsat, MODIS |

**If information is insufficient, DO NOT proceed blindly. Ask clarifying questions:**
```
What is the study area? (e.g., Yellow River Basin, Wuhan city, global scale)
What is the time range? (default: last 5 years)
Do you have a satellite data preference? (recommend Sentinel-2 for urban, Landsat for long-term)
Which journal type? (Chinese Core or SCI)
```

### 1.2 Multi-Round Systematic Literature Retrieval

Execute 3 rounds of `web_search`:

```
Round 1 (Broad): [core topic] + remote sensing + [study area]
  → Understand overall research landscape

Round 2 (Method-focused): [core topic] + [method: Random Forest / U-Net / LandTrendr]
  → Understand technical approaches

Round 3 (Gap mining): [core topic] + limitations / challenges / future directions
  → Discover research gaps
```

**Quality standards:**
- Minimum 15 high-quality papers retrieved
- Final reference list: 25-30 entries (SCI + Chinese core)
- Cover at least 3-5 different methods/models
- Include specific accuracy values (e.g., OA=0.92, R2=0.87)

### 1.3 Structured Literature Information Extraction

For each paper, extract and save as structured JSON:

```json
{
  "title": "Monitoring vegetation dynamics in the Yellow River Basin...",
  "year": 2023,
  "journal": "Remote Sensing of Environment",
  "data_source": {"satellite": "Sentinel-2", "bands": ["B4","B8"], "resolution": "10m"},
  "preprocessing": ["QA60 cloud masking", "atmospheric correction"],
  "algorithm": "Random Forest",
  "accuracy": {"OA": 0.92, "Kappa": 0.89},
  "innovation": "Multi-temporal texture feature fusion",
  "limitation": "Single year data only"
}
```

### 1.4 Research Gap Analysis & Task Refinement

Based on cross-paper comparison, identify 3-5 research gaps and convert each into a concrete GEE-executable task:

| Attribute | Description | Example |
|-----------|-------------|---------|
| **Task ID** | Unique identifier | Task-1 |
| **Task Type** | classification / monitoring / regression / change_detection | monitoring |
| **Target Variable** | Prediction target | NDVI trend slope |
| **Datasets** | GEE dataset IDs + parameters | COPERNICUS/S2_SR_HARMONIZED |
| **Study Area** | Specific boundary geometry | ee.Geometry.Point([114.269,30.562]).buffer(500) |
| **Time Range** | Start-end | 2020-01-01 ~ 2025-06-01 |
| **Baseline Models** | 2-3 literature methods | Random Forest, CART |
| **Improved Model** | This study's innovation | RF with multi-temporal texture |
| **Metrics** | Evaluation criteria | OA, Kappa, F1 or R2, RMSE |
| **Expected Output** | Data product types | classification map, trend map, statistics |

### 1.5 Output: task_list.json

Save to `tasks/task_list.json` for Phase 2 consumption.

---

## Phase 2: GEEPro — Multi-Task Execution with Automatic TIF Download & Figure Generation

### 2.1 Environment Verification

```python
import ee
ee.Initialize(project="your-project-id")
print("GEE Ready")
```

### 2.2 Task Execution Pipeline

For each task, execute the following steps:

#### Step 1: Data Loading & Preprocessing
```python
# Sentinel-2 data loading
s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
      .filterBounds(roi)
      .filterDate(start_date, end_date)
      .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)))

# Add NDVI band
def add_ndvi(img):
    ndvi = img.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return img.addBands(ndvi)
s2_ndvi = s2.map(add_ndvi)
```

#### Step 2: Compute Annual/Seasonal Composites
```python
for year in range(start_year, end_year + 1):
    yearly = s2_ndvi.filterDate(f"{year}-01-01", f"{year}-12-31")
    median_ndvi = yearly.select("NDVI").median().clip(roi)
```

#### Step 3: Download GeoTIFF Files
**CRITICAL: ALWAYS download NDVI/FVC GeoTIFFs for all years.**
```python
url = median_ndvi.getDownloadURL({
    "name": f"{site_name}_ndvi_{year}",
    "scale": 10,
    "region": roi,
    "format": "GEO_TIFF",
    "crs": "EPSG:4326"
})
# Download via requests and save to figures/ndvi_tif/
```

#### Step 4: Compute Statistics
- Mean, std, min, max NDVI per year per site
- Trend analysis (linear regression slope, R2, Mann-Kendall p-value)
- Vegetation grade classification (high/medium/low)
- Change detection (improved/stable/degraded)

#### Step 5: Generate Publication-Quality Figures (300 DPI PNG)
Generate ALL of the following figures automatically:
- **Fig 1**: Study area location map with NDVI baseline
- **Fig 2**: NDVI/FVC time series line chart (both sites, all years)
- **Fig 3**: NDVI spatial comparison (first year vs last year side by side)
- **Fig 4**: Vegetation grade classification bar chart
- **Fig 5**: Change detection bar chart
- **Fig 6**: Multi-year NDVI panel (all years for both sites)

**Figure specifications:**
- Format: PNG, 300 DPI
- Size: 10-12 inches wide
- Colormap: RdYlGn for NDVI spatial maps
- Labels: English (to avoid CJK font issues in matplotlib)

### 2.3 Task Output Directory Structure

```
runs/YYYYMMDD_HHMMSS_topic/
├── summary.json                    # All tasks summary
├── Task-1/
│   ├── code.py                     # Complete GEE script
│   ├── accuracy.json               # Accuracy metrics
│   └── statistics.csv              # Statistical results
├── Task-2/ ...
├── Task-3/ ...
└── Task-4/ ...
```

---

## Phase 3: ResearchX — Complete Manuscript Generation (8000+ Words)

### 3.1 Result Integration

Read all task outputs from Phase 2 and generate cross-comparison tables automatically.

### 3.2 Manuscript Structure (8000+ Words)

The manuscript follows the standard SCI / Chinese-core journal structure below.

#### Title (自动生成)

Format: `基于 [核心方法] 的 [研究对象] [目标变量] [时间范围] 研究`
Example: `基于 Sentinel-2 像元二分模型的武汉龟山蛇山植被覆盖度变化监测研究（2020-2025）`

#### Abstract (300-500 words)

Structure:
```
Background (2-3 sentences): Importance of the research field and existing problem
Objective (1-2 sentences): Scientific question addressed
Methods (3-4 sentences): Data, study area, main methods
Results (5-8 key numerical findings): Include all critical accuracy metrics
Conclusion (1-2 sentences): Scientific significance and application value
```

#### Keywords: 5-8 core terms

#### 1. Introduction (1000-1500 words, 5 paragraphs)

**Paragraph 1 — Grand Background (250-300 words):**
- Importance of the research field
- Remote sensing technology advantages
- Significance of the specific study area
- Cite 3-5 foundational references

**Paragraph 2 — International Progress (250-300 words):**
- Review 5-8 key papers organized by methodology
- Compare their data sources, algorithms, and accuracies
- Identify the best-performing approaches
- Use specific accuracy numbers from literature

**Paragraph 3 — Domestic Progress (150-200 words, for Chinese core):**
- Review Chinese-language studies on similar topics
- Compare with international studies

**Paragraph 4 — Research Gaps (200-250 words):**
- Summarize 2-3 specific limitations of existing work
- Explain why these gaps matter
- Connect gaps to the proposed study

**Paragraph 5 — This Study (150-200 words):**
- Research objectives (numbered list)
- Innovation points (3-5 items)
- Paper structure overview

#### 2. Study Area & Data (800-1000 words)

**2.1 Study Area Overview (300-400 words):**
- Geographic location, coordinates
- Climate, topography, vegetation types
- Ecological and cultural significance
- Include study area map (Fig 1)

**2.2 Data Sources (250-300 words):**
Table format with: dataset, satellite, bands, resolution, time range, purpose

**2.3 Data Preprocessing (250-300 words):**
- Cloud masking method (QA60 / pixel_qa)
- Radiometric calibration and atmospheric correction
- Clipping and compositing methods
- Formula for NDVI:
\[
NDVI = \frac{NIR - Red}{NIR + Red}
\]

#### 3. Methods (1500-2000 words)

**3.n Task-N Name (300-400 words each):**

For each task, include:
- **Principle**: Explain the method's physical/algorithmic basis
- **Formula**: Mathematical expression
- **Implementation**: GEE code snippet (key parts only, not full code)
- **Parameters**: All tunable parameters with their chosen values

**Example formulas to include:**

FVC using Dimidiate Pixel Model:
\[
FVC = \frac{NDVI - NDVI_{soil}}{NDVI_{veg} - NDVI_{soil}}
\]
where NDVI_soil = 0.05 (bare soil NDVI) and NDVI_veg = 0.85 (full vegetation NDVI).

Linear Trend:
\[
y = \beta_0 + \beta_1 t + \varepsilon
\]
where β1 is the trend slope, estimated by ordinary least squares.

Mann-Kendall Test:
\[
S = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} sgn(x_j - x_i)
\]
\[
sgn(x) = \begin{cases}
1 & x > 0 \\
0 & x = 0 \\
-1 & x < 0
\end{cases}
\]

Classification Accuracy Metrics:
\[
OA = \frac{TP + TN}{TP + TN + FP + FN}
\]
\[
Kappa = \frac{p_o - p_e}{1 - p_e}
\]

#### 4. Results & Analysis (2000-2500 words)

**4.n Task-N Results (400-600 words each):**
- **Descriptive text**: Describe the spatial and temporal patterns
- **Table**: Formatted accuracy/results table
- **Figure**: Embedded figure (Fig X) with caption
- **Key numbers**: All critical values highlighted

#### 5. Discussion (800-1000 words)

**5.1 Reliability Analysis (200-250 words):**
- Compare results with existing literature
- Explain consistency or inconsistency
- Discuss data quality and methodological robustness

**5.2 Limitations (200-250 words):**
- Data limitations (resolution, time span, cloud cover)
- Method limitations (assumptions, simplifications)
- Sample and validation limitations

**5.3 Implications (200-250 words):**
- Scientific significance
- Policy/management recommendations
- Practical applications

**5.4 Future Work (200-250 words):**
- Extended time series
- Additional data sources
- Improved methods
- Broader study areas

#### 6. Conclusion (300-400 words)

Numbered points (4-6 items), each containing a specific numerical finding:
```
(1) Key finding with numbers...
(2) Key finding with numbers...
...
```

#### References (25-30 entries)

- Chinese core: GB/T 7714-2015 format
- SCI: APA (default) or MLA format
- At least 20 from Phase 1 literature retrieval
- Remaining 5-10 as supplementary classic references

### 3.3 Figure References in Manuscript

```markdown
<!-- In the manuscript text, reference figures like this: -->

![Fig 1](figures/fig1_study_area.png)
*Fig 1 Study area location and NDVI overview (2020 Sentinel-2 median NDVI)*

![Fig 2](figures/fig2_ndvi_timeseries.png)
*Fig 2 Annual mean NDVI variation for both study sites (2020-2025)*
```

### 3.4 Output Files

```
outputs/YYYYMMDD_HHMMSS_topic_paper/
├── manuscript.md               # Complete manuscript (8000+ words)
├── manuscript.html             # HTML version with rendered tables/figures
├── manuscript.docx             # Word document (with embedded images)
├── figures/                    # All publication-quality figures (300 DPI PNG)
│   ├── fig1_study_area.png
│   ├── fig2_ndvi_timeseries.png
│   ├── fig3_ndvi_comparison.png
│   ├── fig4_vegetation_grade.png
│   ├── fig5_change_detection.png
│   ├── fig6_multiyear_ndvi.png
│   └── ndvi_tif/              # All original GeoTIFF files
│       ├── site_name_ndvi_2020.tif
│       └── ...
├── tables/                     # All data tables (CSV + Markdown)
├── gee_code/                   # Complete GEE scripts
└── README.md                   # Reproduction instructions
```

---

## Quality Gates

| Gate | Standard |
|------|----------|
| **Literature-grounded** | Every method claim cites a real paper from search |
| **Quantified** | Every result includes specific numerical values |
| **Sufficient length** | Manuscript > 6000 words (target 8000+) |
| **Reproducible** | Methods detailed enough to replicate |
| **Embedded figures** | All generated figures inserted into manuscript |
| **Formatted output** | manuscript.md + manuscript.html + manuscript.docx |
| **TIF download** | All NDVI/FVC rasters saved as GeoTIFF |

---

## Error Handling

| Situation | Protocol |
|-----------|----------|
| GEE not authenticated | Output auth command, proceed with dry-run simulation |
| Dataset unavailable | Auto-switch to alternative (S2→L8→MODIS) |
| Memory exceeded | Auto-scale adjustment |
| Network timeout | Retry with exponential backoff (3 attempts) |
| Vague user input | Ask clarifying questions before proceeding |

---

## CLI Reference

```bash
# Full pipeline
python scripts/run_pipeline.py --topic "研究主题" --project PROJECT_ID

# Dry-run (literature + paper only, no GEE)
python scripts/run_pipeline.py --topic "..." --dry-run

# Phase-specific
python scripts/run_pipeline.py --topic "..." --phase literature
python scripts/run_pipeline.py --topic "..." --phase gee
python scripts/run_pipeline.py --topic "..." --phase paper

# Options
--topic TEXT     Research topic (required)
--project TEXT   GEE Project ID (required for Phase 2)
--region TEXT    Study area
--time TEXT      Time range (default: last 5 years)
--tasks INT      Number of tasks 3-5 (default: 4)
--format TEXT    Reference format: gb/apa/mla (default: gb)
--journal TEXT   Journal type: chinese/sci (prompt if not specified)
--no-deep        Disable deep learning
--dry-run        Scheme only, no GEE execution
--phase TEXT     Phase: all/literature/gee/paper
```

---

## Platform Integration

### OpenAI Codex CLI
```bash
Copy-Item -Recurse "PaperForge" "$env:USERPROFILE\.codex\skills\PaperForge"
```

### Claude Desktop
Add to Custom Instructions:
```
You have access to PaperForge skill (github.com/xingguangYan/PaperForge).
Follow the 3-phase workflow in SKILL.md for remote sensing paper automation.
```

### Cline (.clinerules)
```markdown
You have loaded PaperForge skill. Full remote sensing paper generation capability.
Workflow: literature mining → GEE tasks → manuscript (8000+ words) → DOCX output.
```

### Cursor (.cursorrules)
```markdown
PaperForge skill active. For remote sensing research topics, execute the complete 3-phase pipeline.
Always ask for journal type (Chinese core / SCI) before starting.
```

### Windsurf (.windsurfrules)
```
PaperForge skill integrated. End-to-end RS paper automation pipeline.
Before execution: ask journal type + study area + time range + data preference.
After execution: deliver manuscript.md + manuscript.html + manuscript.docx with embedded figures.
```

---

## Dependency Installation

```bash
pip install earthengine-api geemap geopandas pandas numpy matplotlib seaborn requests python-docx rasterio
```

### GEE Authentication
```bash
earthengine authenticate
```

### Proxy Configuration (China)
```powershell
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
```
