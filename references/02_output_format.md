# GeoRS-Pipeline 输出格式规范

## 目录结构

### Phase 2 输出 (GEE 任务执行)
```
runs/YYYYMMDD_HHMMSS_topic/
├── Task-1/
│   ├── code.py           # 完整 GEE Python 脚本
│   ├── RUN.md            # 运行说明
│   ├── result.tif        # 输出栅格
│   ├── statistics.csv    # 统计结果
│   ├── accuracy.json     # 精度评估
│   └── figure.png        # 结果图 (300 DPI)
├── Task-2/
│   └── ...
└── summary.json          # 汇总结果
```

### Phase 3 输出 (论文)
```
outputs/YYYYMMDD_HHMMSS_topic/
├── manuscript.md         # 完整论文草稿
├── figures/              # 结果图 (PNG, 300 DPI)
├── tables/               # 精度表/统计表 (CSV+MD)
├── gee_code/             # 完整 GEE 脚本
├── results_raw/          # 原始栅格/矢量/CSV
└── README.md             # 复现说明
```

## 图表规范

- 图片格式: PNG, 300 DPI
- 三线表格式: Markdown 表格 + CSV
- 图片引用: ![Fig X](path)
- 表格引用: 参见表 X
