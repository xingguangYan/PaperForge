# PaperForge 输出格式规范 (Output Format Reference)

> Referenced by `SKILL.md` §Phase 3. Version: 2.0.

## Phase 2 输出 (GEE task runs)

```
runs/YYYYMMDD_HHMMSS_topic/
├── summary.json               # 所有任务汇总
├── Task-1/
│   ├── code.py                # 完整 GEE Python 脚本
│   ├── RUN.md                 # 运行说明
│   ├── inputs.json            # 输入参数
│   ├── result.tif             # 输出栅格 (GeoTIFF)
│   ├── accuracy.json          # 精度评估指标
│   ├── statistics.csv         # 统计结果
│   └── figure.png             # 可视化结果图 (300 DPI)
├── Task-2/ ...
└── Task-3/ ...
```

## Phase 3 输出 (论文包, v2.0)

```
outputs/YYYYMMDD_HHMMSS_topic/
├── manuscript.md              # 完整论文草稿 (source of truth)
├── manuscript.html            # 样式化 HTML (浏览器直开)
├── manuscript.docx            # Word 文档 (图片内嵌)
├── manuscript_stats.json      # 字数 / 体积 / 时间戳报告
├── figures/                   # 300 DPI PNG
│   ├── fig1_study_area.png
│   ├── fig2_ndvi_timeseries.png
│   ├── fig3_ndvi_comparison.png
│   ├── fig4_vegetation_grade.png
│   ├── fig5_change_detection.png
│   ├── fig6_multiyear_ndvi.png
│   └── ndvi_tif/              # 全部逐年 GeoTIFF
├── tables/                    # CSV + Markdown 表
└── gee_code/                  # 每任务完整 GEE 脚本
```

### offline demo 输出 (scripts/demo.py)

```
outputs/demo/
├── manuscript.md / .html / .docx / manuscript_stats.json
└── figures/fig2_ndvi_timeseries.png, fig4_vegetation_grade.png
```

## 图表规范

| 类型 | 格式 | 分辨率 | 命名 |
|------|------|--------|------|
| 研究区位置图 | PNG | 300 DPI | fig1_study_area.png |
| NDVI/FVC 时序 | PNG | 300 DPI | fig2_ndvi_timeseries.png |
| 空间对比 | PNG | 300 DPI | fig3_ndvi_comparison.png |
| 植被等级 | PNG | 300 DPI | fig4_vegetation_grade.png |
| 变化检测 | PNG | 300 DPI | fig5_change_detection.png |
| 多年面板 | PNG | 300 DPI | fig6_multiyear_ndvi.png |

- 图内文字用英文 (避免 matplotlib 中文缺字形)。
- 精度表: CSV + MD 双份。统计表: CSV + MD 双份。

## 论文引用规范

- 图片: `![Fig 1](figures/fig1_study_area.png)` + 斜体 caption
- 表格: Markdown 表格
- 参考文献: GB/T 7714-2015 (默认), APA, MLA — 由 `scripts/literature.py:format_reference` 生成
