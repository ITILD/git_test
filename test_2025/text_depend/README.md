# Excel 批量处理工具

本项目用于批量读取指定文件夹中的 `.xlsx` 文件，对数据进行处理（如预测值以及数据走向），并输出 `.xlsx`文件至目录。

## 📦 功能特点

- ✅ 自动读取 `input_xlsx/` 目录下所有 Excel 文件  
- ✅ 支持单工作表数据处理（默认读取第一个 sheet）  
- ✅ 自动计算xxxxxxx()  
- ✅ 输出结果保存至 `result_xlsx/`，保留原始文件名  
- ✅ 自动创建缺失目录，错误文件有日志提示

## 🛠️ 环境依赖

- Python 3.8+
- 依赖库：
  - `polars`
  - `openpyxl`


安装命令：
```bash
pip install polars openpyxl

