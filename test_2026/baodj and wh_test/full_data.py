import polars as pl
import numpy as np
from scipy.interpolate import interp1d

def read_excel(path: str) -> list:
    df = pl.read_excel(path, infer_schema_length=0)
    cols_to_convert = ["2", "3", "4", "5", "6"]
    existing_cols = [col for col in cols_to_convert if col in df.columns]

    df = df.with_columns([
        pl.col(col).cast(pl.Float64, strict=False) for col in existing_cols
    ])
    return df.to_numpy().tolist()

def run_process():
    data_list = read_excel("temp/test1.xlsx")
    df = pl.DataFrame(data_list, schema=[f"col_{i}" for i in range(len(data_list[0]))])
    original_columns = ["1", "2", "3", "4", "5", "6"]
    
    if len(original_columns) == len(df.columns):
        df = df.rename({old: new for old, new in zip(df.columns, original_columns)})

    df = df.with_columns(pl.arange(0, len(df)).alias("idx"))
    total_months = len(df)
    date_list = [f"2024-{str(i+1).zfill(2)}" for i in range(total_months)]

    all_months = pl.DataFrame({
        "date": date_list,
        "idx": np.arange(total_months)
    }).with_columns(pl.col("date").str.to_date("%Y-%m"))

    df_full = all_months.join(df, on="idx", how="left")

    def interpolate_column(df, col_name):
        non_null = df.drop_nulls(col_name)
        if len(non_null) < 2:
            return df
        x = np.arange(len(df))
        x_valid = np.arange(len(non_null))
        y_valid = non_null[col_name].to_numpy()
        f = interp1d(x_valid, y_valid, kind="linear", fill_value="extrapolate")
        return df.with_columns(pl.Series(col_name, f(x)))

    for col in ["2", "3", "4", "5", "6"]:
        if col in df_full.columns:
            df_full = interpolate_column(df_full, col)

    df_final = df_full.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("月份")
    ).drop(["date", "idx"])

    # 输出：temp/full_data.xlsx
    df_final.write_excel("temp/full_data.xlsx")
    print("✅ 成员A：已生成 temp/full_data.xlsx")

if __name__ == "__main__":
    run_process()