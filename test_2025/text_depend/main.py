import polars as pl
import numpy as np
from sklearn.linear_model import LinearRegression
# 示例数据
data = {
    "category": ["A", "A", "B", "B", "C"],
    "sales": [100, 150, 200, 50, 300],
    "profit": [20, 30, 40, 10, 60],
    "quantity": [5, 3, 8, 2, 10]
}

df = pl.DataFrame(data)
print("原始数据:")
print(df)

# 1. 所有数值列的总和
print("\n1. 所有数值列总和:")
total_sums = df.select(pl.all().exclude("category").sum())
print(total_sums)

# 2. 按类别分组求和
print("\n2. 按类别分组求和:")
category_sums = df.group_by("category").agg([
    pl.col("sales").sum().alias("total_sales"),
    pl.col("profit").sum().alias("total_profit"),
    pl.col("quantity").sum().alias("total_quantity")
])
print(category_sums)

# 3. 行方向求和
print("\n3. 每行数值总和:")
df_with_total = df.with_columns(
    pl.sum_horizontal(pl.col(pl.NUMERIC_DTYPES)).alias("row_total")
)
print(df_with_total)

# 4. 获取单个总和值
total_sales = df.select(pl.col("sales").sum()).item()
print(f"\n4. 销售总额: {total_sales}")

# 5. 线性回归预测

# 根据图片数据创建DataFrame
data = {
    '月份': ['一月', '二月', '三月', '四月'],
    '总和': [34+23+4+3+2+4, 66+77+6+7+6+6, 86+7+7+9+6+12, 123+112+21+14+7+18]
}

df = pl.DataFrame(data)
print("1-4月总和数据：")
print(df)

# 将月份转换为数值
month_map = {'一月': 1, '二月': 2, '三月': 3, '四月': 4}
df['月份数值'] = df['月份'].map(month_map)

# 使用线性回归预测五月总和
X = df[['月份数值']]
y = df['总和']

model = LinearRegression()
model.fit(X, y)

# 预测五月（月份=5）
may_pred = model.predict([[5]])[0]

print(f"\n五月总和预测结果：{may_pred:.0f}")
print(f"回归方程：总和 = {model.intercept_:.1f} + {model.coef_[0]:.1f} × 月份")

if __name__ == "__main__":
    pass
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




