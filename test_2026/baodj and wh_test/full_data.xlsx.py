import polars as pl
import numpy as np
from scipy.interpolate import interp1d

# 1. 读取文件
df = pl.read_excel(r"C:\Users\HP\OneDrive\Desktop\workspace\test\git_test\test_2026\baodj and wh_test\temp\test1.xlsx")
print("✅ 原始数据读取成功，预览：")
print(df)

# 2. 把列2-6转成浮点数，处理null值
for col in ["2", "3", "4", "5", "6"]:
    df = df.with_columns(pl.col(col).cast(pl.Float64))

# 3. 用序号生成虚拟月份
df = df.with_columns(
    pl.arange(0, len(df)).alias("idx")
)

# 生成虚拟月份序列
all_months = pl.DataFrame({
    "date": ["2024-01", "2024-02", "2024-03"],
    "idx": [0, 1, 2]
}).with_columns(pl.col("date").str.to_date("%Y-%m"))

# 左连接补全
df_full = all_months.join(df, on="idx", how="left")
print("\n✅ 虚拟月份补全完成，预览：")
print(df_full)

# 4. 插值补全数值列
def interpolate_column(df, col_name):
    non_null = df.filter(pl.col(col_name).is_not_null())
    if len(non_null) < 2:
        print(f"⚠️ {col_name}数据不足，无法插值，保留原数据")
        return df
    
    x = np.arange(len(df))
    x_valid = np.array(non_null.with_columns(pl.arange(0, len(df)).alias("idx"))["idx"])
    y_valid = np.array(non_null[col_name])
    f = interp1d(x_valid, y_valid, kind="linear", fill_value="extrapolate")
    return df.with_columns(pl.Series(col_name, f(x)))

for col in ["2", "3", "4", "5", "6"]:
    df_full = interpolate_column(df_full, col)

print("\n✅ 插值补全完成，预览：")
print(df_full)

# 5. 生成最终文件（用CSV格式，纯Polars支持）
df_final = df_full.with_columns(
    pl.col("date").dt.strftime("%Y-%m").alias("月份")
).drop(["date", "idx"])

# 这里改成write_csv，零依赖
df_final.write_csv("full_data.csv")
print("\n🎉 成功！完整数据已生成:full_data.csv")