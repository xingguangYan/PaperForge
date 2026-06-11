# GeoRS-Pipeline 详细工作流

## 三个阶段

### Phase 1: ResearchX 文献调研
1. 解析用户输入 → 提取关键要素
2. 多轮 web_search 文献检索 → 关键词扩展
3. 文献信息结构化提取
4. 研究缺口识别 → 3-5 个任务
5. 输出 task_list.json

### Phase 2: GEEPro 自动执行
1. 环境验证 (check_environment.py)
2. 对每个任务：
   - 数据加载 → 预处理 → 特征工程
   - 模型训练/推理 → 精度评估
   - 结果导出（栅格/矢量/统计/图表）
3. 汇总结果

### Phase 3: ResearchX 论文生成
1. 读取所有任务输出
2. 按标准论文结构生成草稿
3. 自动插入图表和表格
4. 格式化参考文献
5. 输出完整论文包

## 参数传递

Phase 1 输出 task_list.json → Phase 2 读取执行
Phase 2 输出 runs/ 目录 → Phase 3 读取生成论文
