import polars as pl
import numpy as np
from scipy.interpolate import interp1d
import os

def read_excel(path: str) -> pl.DataFrame:
    """读取原始 Excel（无表头），列名自动为 column_1 ~ column_6"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    df = pl.read_excel(path, has_header=False)
    if df.width < 6:
        raise ValueError(f"Excel 列数不足6，实际为 {df.width}")
    # 只保留前6列
    df = df.select(pl.all().head(6))
    # 列名已经是 column_1, column_2, ..., column_6
    # 将第2~6列（对应 column_2 到 column_6）转为 Float64
    for i in range(2, 7):
        col_name = f"column_{i}"
        df = df.with_columns(
            pl.col(col_name).cast(pl.Float64, strict=False).alias(col_name)
        )
    # 重命名为业务列名 "1" ~ "6"
    rename_map = {f"column_{j}": str(j) for j in range(1, 7)}
    df = df.rename(rename_map)
    return df

def interpolate_column(df: pl.DataFrame, col_name: str) -> pl.DataFrame:
    """使用线性插值（含外推）填充缺失值，基于 'idx' 列的真实位置"""
    non_null = df.drop_nulls(col_name)
    if len(non_null) < 2:
        return df  # 不足两个点无法插值
    x_all = df["idx"].to_numpy()
    x_valid = non_null["idx"].to_numpy()
    y_valid = non_null[col_name].to_numpy()
    f = interp1d(x_valid, y_valid, kind="linear", fill_value="extrapolate")
    y_filled = f(x_all)
    return df.with_columns(pl.Series(col_name, y_filled))

def run_process():
    data_path = "temp/test1.xlsx"
    print(f"读取原始数据: {data_path}")
    df_raw = read_excel(data_path)

    # 添加原始行索引（用于插值定位）
    df_raw = df_raw.with_columns(pl.arange(0, len(df_raw)).alias("idx"))
    total_months = len(df_raw)
    date_list = [f"2024-{str(i+1).zfill(2)}" for i in range(total_months)]

    all_months = pl.DataFrame({
        "date": date_list,
        "idx": np.arange(total_months)
    }).with_columns(pl.col("date").str.to_date("%Y-%m"))

    df_full = all_months.join(df_raw, on="idx", how="left")

    # 对列 "2"~"6" 插值
    for col in ["2", "3", "4", "5", "6"]:
        if col in df_full.columns:
            df_full = interpolate_column(df_full, col)

    df_final = df_full.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("月份")
    ).select(["月份", "2", "3", "4", "5", "6"])

    os.makedirs("temp", exist_ok=True)
    output_path = "temp/full_data.xlsx"
    df_final.write_excel(output_path)
    print(f"✅ 成员A：已生成 {output_path}")

if __name__ == "__main__":
    run_process()