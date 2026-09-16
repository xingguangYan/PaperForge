---
name: paperforge
description: >-
  End-to-end remote sensing research automation. Given a natural-language
  research topic, PaperForge runs a 3-phase pipeline: (1) multi-round
  literature mining and research-gap analysis, (2) Google Earth Engine (GEE)
  execution that downloads GeoTIFF rasters and computes statistics, and (3)
  generation of a full 8000+ word SCI/Chinese-core manuscript with formulas,
  figures, tables, and references, exported as Markdown + HTML + DOCX. Use
  when the user wants to write, draft, or automate a remote sensing,
  geospatial, Earth-observation, NDVI/vegetation, land-cover, or GEE-based
  research paper; asks to go "from topic/title to manuscript/paper"; requests
  SCI journal or Chinese-core (中文核心) paper writing, literature review, or
  experiment design; or mentions terms like GEE, Sentinel-2, Landsat, MODIS,
  NDVI, remote sensing paper, or 论文/遥感/自动写论文/一键论文.
license: MIT
compatibility: >-
  Requires Python 3.8+; Google Earth Engine account & `earthengine authenticate`
  for Phase 2 (optional - dry-run works without it). Network access needed for
  literature search and GEE. Works in Claude Code, OpenAI Codex CLI, Cline,
  Cursor, Windsurf, GitHub Copilot.
metadata:
  version: "2.0.0"
  author: "xingguangYan"
  homepage: "https://github.com/xingguangYan/PaperForge"
  release_page: "https://github.com/xingguangYan/PaperForge/releases"
allowed-tools: web_search, fetch, image_search, bash, python, write, edit, read
---

# PaperForge — Remote Sensing Research Pipeline

> **"Topic in. Paper out."** — from a natural-language topic to an 8000+ word
> manuscript (Markdown + HTML + DOCX) with GEE-computed figures and tables.

PaperForge integrates two engines:

| Engine | Role |
|--------|------|
| **ResearchX** | Literature mining, experiment design, manuscript writing |
| **GEEPro** | Google Earth Engine execution, raster download, statistics, figures |

Operate in **three phases** (details of each phase are in
[references/01_workflow.md](references/01_workflow.md)):

1. **Phase 1 — ResearchX**: parse the topic → multi-round literature search →
   structured extraction → research gaps → 3-5 GEE tasks (`tasks/task_list.json`).
2. **Phase 2 — GEEPro**: authenticate GEE → download NDVI/FVC GeoTIFFs for all
   years → compute statistics → generate 300-DPI figures.
3. **Phase 3 — ResearchX**: write the 8000+ word manuscript → export
   `manuscript.md` + `manuscript.html` + `manuscript.docx`.

> Use the bundled Python modules (they are tested and deterministic — do not
> hand-write replacements). Import them with a `sys.path` shim into `scripts/`
> when running inside a notebook or inline session.

---

## 0. Before you begin — mandatory setup questions

**ALWAYS ask before Phase 1.** Do not guess. Ask:

1. **Journal type** — 中文核心期刊 (Chinese Core) or SCI?
   - 中文核心: ~6000-8000 字, 中英文摘要, GB/T 7714-2015 参考文献.
   - SCI: ~8000-10000 字, 英文摘要 + Graphical Abstract, APA/MLA 参考文献.
2. **Study area** (place name or coordinates) and **time range** (default: last 5 years).
3. **Satellite data preference** (Sentinel-2 / Landsat / MODIS — recommend Sentinel-2 at 10 m).

If any is missing or ambiguous, ask clarifying questions before proceeding.

---

## Phase 1 — Literature mining & task design (ResearchX)

1. Extract the five elements from the topic: core object, target variable,
   time range, spatial range, data preference. See
   [references/01_workflow.md](references/01_workflow.md) §Input Parsing.
2. Run **3 rounds** of `web_search` (broad → method-focused → gap mining).
3. Extract each paper into the JSON schema in
   [templates/task_template.json](templates/task_template.json) — fields:
   title, year, journal, data_source, algorithm, accuracy, innovation, limitation.
4. Validate the corpus with `scripts/literature.py`:

   ```python
   from literature import validate_corpus
   report = validate_corpus(papers)   # requires >=15 papers, >=3 methods
   ```

   - Minimum **15 papers**; final references **25-30**; cover **3-5 methods**.
   - Every method claim must cite a real retrieved paper; keep accuracy numbers
     (OA, Kappa, R², RMSE).
5. Convert 3-5 research gaps into GEE tasks and write `tasks/task_list.json`
   (see `scripts/gee_tasks.py:build_task` and the template).
6. Output: `tasks/task_list.json` consumed by Phase 2.

---

## Phase 2 — GEE execution (GEEPro)

Use `scripts/gee_tasks.py` (idempotent building blocks — compose, don't rewrite):

| Function | Purpose |
|----------|---------|
| `initialize(project)` | Authenticate & initialize Earth Engine |
| `point_roi(lon, lat, buffer)` / `to_geometry(region)` | ROI construction |
| `masked_sentinel2(roi, start, end)` | Cloud-masked S2 + NDVI/FVC/NDWI |
| `collection_with_fallback(ds, roi, start, end)` | S2 → Landsat → MODIS fallback |
| `annual_median(col, year, band)` | Annual median composite |
| `roi_stats(image, roi)` | Mean/std/min/max/median/count |
| `linear_trend(col, band)` | Per-pixel linear fit trend |
| `vegetation_grade(ndvi)` / `change_detection(a, b)` | Classification |
| `download_tif(image, roi, filename)` | GeoTIFF download w/ retry |

Workflow per task:

1. `initialize(project=...)` — on failure print the auth command and fall back
   to dry-run simulation (see Error Handling below).
2. Load/preprocess data → compute annual medians → **download GeoTIFFs for all
   years and sites** to `figures/ndvi_tif/` (this is a hard requirement).
3. Compute statistics (roi stats, linear trend + Mann-Kendall).
4. Generate the 6 standard figures with `scripts/render_figures.py`
   (300 DPI PNG, English labels to avoid CJK font issues).
5. Save `runs/YYYYMMDD_HHMMSS_topic/summary.json` for Phase 3.

If `--dry-run` or no `--project`: mark results as **simulated** and proceed.

---

## Phase 3 — Manuscript generation (ResearchX)

Structural targets (full rubric in [references/01_workflow.md](references/01_workflow.md) §Manuscript):

| Section | Length | Content |
|---------|--------|---------|
| Title | auto | `[Method]-based [Object] [Variable] [Time]` |
| Abstract | 300-500 w | Background→Objective→Methods→Results→Conclusion |
| 1. Introduction | 1000-1500 w | 5 paragraphs, 3-5+8 citations |
| 2. Study Area & Data | 800-1000 w | location, data table, preprocessing, NDVI formula |
| 3. Methods | 1500-2000 w | per task: principle, formula, GEE code, parameters |
| 4. Results | 2000-2500 w | per task: text + table + figure + key numbers |
| 5. Discussion | 800-1000 w | reliability, limitations, implications, future |
| 6. Conclusion | 300-400 w | 4-6 numbered findings with values |
| References | 25-30 | GB/T 7714-2015 or APA/MLA |

**Always** use `scripts/paper_writer.py` for export — it produces the md/html/docx
+ `manuscript_stats.json` (word count) with graceful degradation:

```python
from demo_data import build_results  # or your own `results` dict
from paper_writer import write_outputs
paths = write_outputs(results, "outputs/<name>")
```

Output layout: see [references/02_output_format.md](references/02_output_format.md).

---

## Quality gates

| Gate | Standard |
|------|----------|
| Literature-grounded | Every method claim cites a real retrieved paper |
| Quantified | Every result carries explicit numbers (OA, Kappa, R², RMSE) |
| Sufficient length | > 6000 words (target 8000+) — checked by `count_words` |
| Reproducible | Methods detailed enough to replicate |
| Figures embedded | All generated figures referenced in the manuscript |
| TIF download | Every NDVI/FVC raster saved as GeoTIFF |
| Multi-format | manuscript.md + manuscript.html + manuscript.docx |

---

## Error handling

| Situation | Protocol |
|-----------|----------|
| GEE not authenticated | print `earthengine authenticate`, continue in dry-run (simulated results) |
| Dataset unavailable | fall back S2 → Landsat 8/9 → MODIS (`collection_with_fallback`) |
| Memory exceeded | increase `scale`, shrink ROI, `bestEffort=True` |
| Network timeout | 3 retries, exponential backoff (built into `download_tif`) |
| Vague user input | ask clarifying questions before proceeding |

---

## Quick commands

```bash
# Full pipeline (needs GEE project + auth)
python scripts/run_pipeline.py --topic "Vegetation change in Wuhan" --project ee-you

# Literature + paper only, no GEE
python scripts/run_pipeline.py --topic "..." --dry-run

# Phase-specific
python scripts/run_pipeline.py --topic "..." --phase literature
python scripts/run_pipeline.py --topic "..." --phase gee
python scripts/run_pipeline.py --topic "..." --phase paper

# Offline smoke demo — proves figures + md + html + docx on any machine
python scripts/demo.py

# Offline test suite
python scripts/test_pipeline.py

# Environment check
python scripts/check_environment.py --project ee-you
```

---

## Platform install

- **OpenAI Codex CLI** — `python scripts/package_codex.py --target ~/.codex/skills`,
  then invoke as `$paperforge`.
- **Claude Code** — copy folder to `~/.claude/skills/PaperForge` (or
  `.claude/skills/PaperForge`).
- **Cline / Cursor / Windsurf / Copilot** — add the one-paragraph instruction
  block shown in [references/01_workflow.md](references/01_workflow.md) §Platform.

---

## Versioning & attribution

This skill is versioned via GitHub Releases
([https://github.com/xingguangYan/PaperForge/releases](https://github.com/xingguangYan/PaperForge/releases)).
Pin to a release tag for reproducibility; `main` tracks the latest. MIT license —
see [LICENSE](LICENSE).
