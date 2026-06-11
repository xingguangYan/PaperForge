# PaperForge 输出格式规范

## 目录结构

### Phase 2 输出 (GEE 任务执行)

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

### Phase 3 输出 (论文包)

```
outputs/YYYYMMDD_HHMMSS_topic/
├── manuscript.md              # 完整论文草稿
├── figures/                   # 所有结果图 (PNG, 300 DPI)
│   ├── fig1_study_area.png
│   ├── fig2_task1_result.png
│   └── fig3_task2_trend.png
├── tables/                    # 精度表 / 统计表
│   ├── table1_accuracy.csv
│   ├── table1_accuracy.md
│   └── table2_statistics.csv
├── gee_code/                  # 每个任务完整 GEE 脚本
│   ├── task1_code.py
│   ├── task2_code.py
│   └── task3_code.py
├── results_raw/               # 原始输出数据
│   ├── task1_result.tif
│   └── task2_statistics.csv
└── README.md                  # 复现说明
```

## 图表规范

| 类型 | 格式 | 分辨率 | 命名规则 |
|------|------|--------|---------|
| 研究区位置图 | PNG | 300 DPI | fig1_study_area.png |
| 任务结果图 | PNG | 300 DPI | fig2_taskN_result.png |
| 趋势/时序图 | PNG | 300 DPI | fig3_taskN_trend.png |
| 精度表 | CSV + MD | - | table1_accuracy.csv |
| 统计表 | CSV + MD | - | table2_statistics.csv |

## 论文引用规范

- 图片: `![Fig 1](figures/fig1_study_area.png)`
- 表格: Markdown 表格格式
- 参考文献: GB/T 7714-2025 (默认), APA, MLA
