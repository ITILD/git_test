# 先导入库
import polars as pl
from scipy.interpolate import interp1d
import numpy as np

# ----------------------
# 1. 读取你的原始Excel文件
# ----------------------

df = pl.read_excel("temp/test1.xlsx")  
print("原始数据预览：")
print(df)

# ----------------------
# 2. 补全缺失的月份（关键步骤）
# ----------------------
# 假设你的数据里有一列叫"日期"，格式是 2024-01、2024-02 这样的年月
# 先把日期列转成标准格式
df = df.with_columns(
    pl.col("日期").str.to_date("%Y-%m").alias("date")
)

# 生成完整的月份序列（从数据的第一个月到最后一个月）
start_date = df["date"].min()
end_date = df["date"].max()
all_months = pl.date_range(start_date, end_date, interval="1mo", eager=True).to_frame("date")

# 把原始数据和完整月份做左连接，补全缺失的月份
df_full = all_months.join(df, on="date", how="left")
print("补全缺失月份后：")
print(df_full)

# ----------------------
# 3. 用scipy做插值补全数值（比如销量、金额这些列）
# ----------------------
# 假设你要补的列叫"销量"，把它改成你自己的列名
def interpolate_column(df, col_name):
    # 去掉空值，拿到非空的x（月份序号）和y（数值）
    non_null = df.filter(pl.col(col_name).is_not_null())
    if len(non_null) < 2:
        print(f"{col_name}列数据太少，无法插值")
        return df
    
    # 把日期转成数字（比如从0开始的序号）
    x = np.arange(len(df))
    x_valid = np.array(non_null.with_columns(pl.arange(0, len(df)).alias("idx"))["idx"])
    y_valid = np.array(non_null[col_name])
    
    # 线性插值
    f = interp1d(x_valid, y_valid, kind="linear", fill_value="extrapolate")
    y_interp = f(x)
    
    # 把插值结果放回DataFrame
    df = df.with_columns(pl.Series(col_name, y_interp))
    return df

# 对需要补全的列执行插值（这里写你要补的列名，多个列可以写多次）
df_full = interpolate_column(df_full, "销量")

# ----------------------
# 4. 生成最终的 full_data.xlsx
# ----------------------
# 把date列转回年月格式，方便看
df_full = df_full.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("月份")).drop("date")

# 保存成Excel，这就是你要提交的交付物
df_full.write_excel("full_data.xlsx")
print("✅ 完整数据已生成:full_data.xlsx")