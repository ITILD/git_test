import polars as pl

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


if __name__ == "__main__":
    pass
