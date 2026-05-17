import polars as pl
import numpy as np
from scipy.interpolate import interp1d

# ----------------------
# 1. 读取你的原始Excel文件
# ----------------------
def read_excel(path:str) -> list:
    """读取Excel并返回list"""
    df = pl.read_excel(path, infer_schema_length=0)  # 先不推断类型，全部当字符串
    
    # 把列2-6转成浮点数，处理null值
    cols_to_convert = ["2", "3", "4", "5", "6"]
    existing_cols = [col for col in cols_to_convert if col in df.columns]
    
    # 批量转换为浮点数，转换失败的设为null
    df = df.with_columns([
        pl.col(col).cast(pl.Float64, strict=False) for col in existing_cols
    ])
    
    # 转换为list并返回
    data = df.to_numpy().tolist()
    return data

# 主处理逻辑
if __name__ == "__main__":
    # 读取数据（返回list）
    data_list = read_excel("temp/test1.xlsx")
    
    # 将list转换回DataFrame进行处理
    df = pl.DataFrame(data_list, schema=[f"col_{i}" for i in range(len(data_list[0]))])
    
    # 重命名列为原始列名（如果你知道原始列名的话）
    # 假设原始列名是 col1, col2, ... 或者根据你的实际列名修改
    original_columns = ["1", "2", "3", "4", "5", "6"]  # 根据实际情况修改
    if len(original_columns) == len(df.columns):
        df = df.rename({old: new for old, new in zip(df.columns, original_columns)})
    
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
        x_valid = non_null.select(pl.arange(0, len(non_null)).alias("idx"))["idx"].to_numpy()
        y_valid = non_null[col_name].to_numpy()
        f = interp1d(x_valid, y_valid, kind="linear", fill_value="extrapolate")
        return df.with_columns(pl.Series(col_name, f(x)))
    
    for col in ["2", "3", "4", "5", "6"]:
        if col in df_full.columns:
            df_full = interpolate_column(df_full, col)
    
    print("\n✅ 插值补全完成，预览：")
    print(df_full)
    
    # 5. 生成最终文件
    df_final = df_full.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("月份")
    ).drop(["date", "idx"])
    
    # 保存为CSV
    df_final.write_csv("full_data.csv")
    print("\n🎉 成功！完整数据已生成: full_data.csv")
    
    # 如果需要最终结果也是list
    final_list = df_final.to_numpy().tolist()
    print(f"\n📌 最终结果类型: {type(final_list)},是list: {isinstance(final_list, list)}")