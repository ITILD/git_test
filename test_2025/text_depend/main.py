import json
import pandas as pd
import os

# ========================
# 配置路径（建议用原始字符串 r"" 避免转义）
# ========================
json_path = r'D:\baizhan_program\1115\gitee\git_test\test_2025\text_depend\input_xlsx\data.json'
output_path = r'D:\baizhan_program\1115\gitee\git_test\test_2025\text_depend\result_xlsx\multi_sheet_output.xlsx'

# 确保输出目录存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# ========================
# 读取 JSON 文件
# ========================
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"❌ 错误：找不到 JSON 文件\n路径: {json_path}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"❌ 错误：JSON 格式无效\n{e}")
    exit(1)

# ========================
# 判断 JSON 结构类型
# ========================
if isinstance(data, dict):
    # ✅ 情况 A：顶层是字典 → 每个 key 是一个 sheet
    sheet_data = data
elif isinstance(data, list):
    # ✅ 情况 B：顶层是列表 → 默认放在一个叫 "Sheet1" 的 sheet 中
    sheet_data = {"Sheet1": data}
else:
    print("❌ 不支持的 JSON 根类型（必须是对象或数组）")
    exit(1)

# ========================
# 写入多 Sheet Excel
# ========================
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for sheet_name, records in sheet_data.items():
        if not isinstance(records, list):
            # 只能处理  列表 of 字典？
            print(f"⚠️ 警告：'{sheet_name}' 不是列表，跳过该 sheet")
            continue
        try:
            # 展平嵌套 JSON 结构，转换为 DataFrame
            df = pd.json_normalize(records)
            # 自动截断过长的 sheet 名（Excel 限制 ≤31 字符）
            safe_sheet_name = str(sheet_name)[:31]
            # 转为 Excel
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
            print(f"✅ 已写入工作表: {safe_sheet_name} ({len(df)} 行)")
        except Exception as e:
            print(f"❌ 写入 '{sheet_name}' 失败: {e}")




