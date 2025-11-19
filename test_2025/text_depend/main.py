# 从Excel文件读取数据的示例
import datetime as dt
from pathlib import Path
import polars as pl
from sklearn.linear_model import LinearRegression


def read_excel_data(file_path):
    """从Excel文件读取数据并返回Polars DataFrame"""
    try:
        # 使用Polars的read_excel函数读取Excel文件
        # 注意：需要安装相关依赖，如openpyxl或xlsx2csv
        df = pl.read_excel(file_path)
        return df
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        print("请确保已安装openpyxl或xlsx2csv依赖")
        # 如果读取失败，返回一个示例DataFrame
        return pl.DataFrame(
            {
                "name": ["first month", "second month", "third month", "fourth month"],
                "birthdate": [
                    dt.date(1997, 1, 10),
                    dt.date(1985, 2, 15),
                    dt.date(1983, 3, 22),
                    dt.date(1981, 4, 30),
                ],
                "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
                "height": [1.56, 1.77, 1.65, 1.75],  # (m)
            }
        )
# 示例Excel文件路径（请根据实际情况修改）
excel_file_path = r"input_xlsx/input.xlsx"
# 读取Excel数据
df = read_excel_data(excel_file_path)
print("读取的数据:")
print(df)

    


# # 根据图片中的准确数据创建DataFrame
# data = {
#     "月份": ["一月", "二月", "三月", "四月"],
#     "鸡": [34, 66, 86, 123],
#     "鸭": [23, 77, 7, 112],
#     "大象": [4, 6, 7, 21],
#     "独角兽": [3, 7, 9, 14],
#     "猛犸象": [2, 6, 6, 7],
#     "霸王龙": [4, 6, 12, 18]
# }

# df = pl.DataFrame(data)
# print("原始数据:")
# print(df)

# # 1. 计算每月总和（所有动物的总和）
# print("\n1. 每月总和计算:")
# monthly_totals = df.with_columns(
#     pl.sum_horizontal(pl.exclude("月份")).alias("每月总和")
# ).select(["月份", "每月总和"])

# print(monthly_totals)

# # 2. 各动物1-4月总计
# print("\n2. 各动物总计（1-4月）:")
# animal_totals = df.select(
#     pl.exclude("月份").sum()
# ).melt(variable_name="动物", value_name="总计")

# print(animal_totals)

# # 3. 添加月份数值列用于回归分析
# df_for_regression = monthly_totals.with_columns(
#     pl.col("月份").replace({"一月": 1, "二月": 2, "三月": 3, "四月": 4}).alias("月份数值")
# )

# print("\n3. 回归分析数据:")
# print(df_for_regression)

# # 4. 使用线性回归预测五月总和
# # 准备数据
# X = df_for_regression.select("月份数值").to_numpy()
# y = df_for_regression.select("每月总和").to_numpy().flatten()

# # 训练模型
# model = LinearRegression()
# model.fit(X, y)

# # 预测五月（月份=5）
# may_prediction = model.predict([[5]])[0]

# print(f"\n4. 五月总和预测结果:")
# print(f"五月总和预测: {may_prediction:.0f}")
# print(f"回归方程: 总和 = {model.intercept_:.1f} + {model.coef_[0]:.1f} × 月份")

# # 5. 显示详细的每月数据
# print(f"\n5. 详细每月数据:")
# detailed_analysis = df.with_columns(
#     pl.sum_horizontal(pl.exclude("月份")).alias("每月总和")
# )
# print(detailed_analysis)

# # 6. 增长率分析
# print(f"\n6. 月度增长率分析:")
# growth_analysis = df_for_regression.with_columns([
#     pl.col("每月总和").diff().alias("月增长量"),
#     ((pl.col("每月总和").diff() / pl.col("每月总和").shift(1)) * 100).round(2).alias("月增长率(%)")
# ])
# print(growth_analysis)

# # 7. 最终预测报告
# print(f"\n{'='*50}")
# print(f"📊 五月预测报告")
# print(f"{'='*50}")
# print(f"基于1-4月数据:")
# for i in range(len(df_for_regression)):
#     month = df_for_regression["月份"][i]
#     total = df_for_regression["每月总和"][i]
#     print(f"  {month}: {total}")

# print(f"\n📈 预测结果:")
# print(f"  五月总和预测: {may_prediction:.0f}")
# print(f"  平均月增长: {model.coef_[0]:.1f}")
# print(f"  预测置信度: 基于线性回归模型，R² = {model.score(X, y):.3f}")



# ========================
def main():
    input_dir = Path("input_xlsx")
    output_dir = Path("result_xlsx")
    # 确保输入目录存在
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        return
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 获取所有 .xlsx 文件（不包括临时 ~$ 文件）
    xlsx_files = [f for f in input_dir.glob("*.xlsx") if not f.name.startswith("~$")]

    if not xlsx_files:
        print(f"📂 输入目录中没有找到 .xlsx 文件: {input_dir}")
        return

    print(f"🔍 找到 {len(xlsx_files)} 个 Excel 文件，开始处理...")
# 逐个处理文件,未完成




    for file_path in xlsx_files:
        try:
            print(f"\n📄 正在处理: {file_path.name}")
            df = read_excel_data(file_path)

            # 构建输出路径（保持文件名一致）
            output_file = output_dir / file_path.name

            # 写入 Excel（单工作表）
            df.write_excel(output_file, worksheet="Data")
            print(f"✅ 已写入: {output_file}")

        except Exception as e:
            print(f"❌ 处理文件 {file_path.name} 时发生未预期错误: {e}")
    print("\n🎉 所有文件处理完成！")

if __name__ == "__main__":
    main()


