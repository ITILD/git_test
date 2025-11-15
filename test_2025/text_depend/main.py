# 读取json内容并打印到excel表格中
import json
import pandas as pd

# 1. 读取 JSON 文件（或直接使用 JSON 字符串）
with open('D:\\baizhan_program\\1115\\gitee\\git_test\\test_2025\\text_depend\\input_xlsx\\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 2. 转换为 DataFrame（二维表格数据）

# 情况 A：JSON 是列表 of 字典（最常见）
df = pd.DataFrame(data)
# 情况 B：JSON 是嵌套结构，自动展平嵌套结构
# df = pd.json_normalize(data)

# 3. 使用openpyxl把DataFrame写入 Excel
df.to_excel('D:\\baizhan_program\\1115\\gitee\\git_test\\test_2025\\text_depend\\result_xlsx\\output.xlsx', index=False, engine='openpyxl')
print("✅ 已成功导出到 output.xlsx")


