# Excel月度缺失数据插值与可视化项目
本项目使用 `polars` 进行Excel高效数据处理，`scipy` 实现科学插值，自动补全时间序列中缺失的月份；
通过 `matplotlib` 实现可视化对比，清晰展示插值前后数据差异，完成数据清洗与交付展示。

## 技术栈
- 数据处理：polars
- 插值计算：scipy
- 可视化：matplotlib
- 文件读写：openpyxl

## 成员分工表
| 角色 | 姓名 | 核心工作 | 交付物 |
|------|------|------|----------|--------|
| A | baodj | 读取Excel、补全缺失月份、scipy插值、输出完整表格 | full_data.xlsx |
| B | wenhan |  生成对比折线图、美化图表、编写项目文档、Gitee仓库提交 | trend_compare.png、README.md、Gitee仓库 |

## 运行步骤
1. 安装依赖
```bash
pip install polars openpyxl scipy matplotlib
