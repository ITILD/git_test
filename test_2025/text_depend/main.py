import polars as pl
import numpy as np
from sklearn.linear_model import LinearRegression

# 根据图片中的准确数据创建DataFrame
data = {
    "月份": ["一月", "二月", "三月", "四月"],
    "鸡": [34, 66, 86, 123],
    "鸭": [23, 77, 7, 112],
    "大象": [4, 6, 7, 21],
    "独角兽": [3, 7, 9, 14],
    "猛犸象": [2, 6, 6, 7],
    "霸王龙": [4, 6, 12, 18]
}

df = pl.DataFrame(data)
print("原始数据:")
print(df)

# 1. 计算每月总和（所有动物的总和）
print("\n1. 每月总和计算:")
monthly_totals = df.with_columns(
    pl.sum_horizontal(pl.exclude("月份")).alias("每月总和")
).select(["月份", "每月总和"])

print(monthly_totals)

# 2. 各动物1-4月总计
print("\n2. 各动物总计（1-4月）:")
animal_totals = df.select(
    pl.exclude("月份").sum()
).melt(variable_name="动物", value_name="总计")

print(animal_totals)

# 3. 添加月份数值列用于回归分析
df_for_regression = monthly_totals.with_columns(
    pl.col("月份").replace({"一月": 1, "二月": 2, "三月": 3, "四月": 4}).alias("月份数值")
)

print("\n3. 回归分析数据:")
print(df_for_regression)

# 4. 使用线性回归预测五月总和
# 准备数据
X = df_for_regression.select("月份数值").to_numpy()
y = df_for_regression.select("每月总和").to_numpy().flatten()

# 训练模型
model = LinearRegression()
model.fit(X, y)

# 预测五月（月份=5）
may_prediction = model.predict([[5]])[0]

print(f"\n4. 五月总和预测结果:")
print(f"五月总和预测: {may_prediction:.0f}")
print(f"回归方程: 总和 = {model.intercept_:.1f} + {model.coef_[0]:.1f} × 月份")

# 5. 显示详细的每月数据
print(f"\n5. 详细每月数据:")
detailed_analysis = df.with_columns(
    pl.sum_horizontal(pl.exclude("月份")).alias("每月总和")
)
print(detailed_analysis)

# 6. 增长率分析
print(f"\n6. 月度增长率分析:")
growth_analysis = df_for_regression.with_columns([
    pl.col("每月总和").diff().alias("月增长量"),
    ((pl.col("每月总和").diff() / pl.col("每月总和").shift(1)) * 100).round(2).alias("月增长率(%)")
])
print(growth_analysis)

# 7. 最终预测报告
print(f"\n{'='*50}")
print(f"📊 五月预测报告")
print(f"{'='*50}")
print(f"基于1-4月数据:")
for i in range(len(df_for_regression)):
    month = df_for_regression["月份"][i]
    total = df_for_regression["每月总和"][i]
    print(f"  {month}: {total}")

print(f"\n📈 预测结果:")
print(f"  五月总和预测: {may_prediction:.0f}")
print(f"  平均月增长: {model.coef_[0]:.1f}")
print(f"  预测置信度: 基于线性回归模型，R² = {model.score(X, y):.3f}")

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




