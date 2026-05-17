import polars as pl

# 读取文件
df = pl.read_csv("full_data.csv")

# 转成 list
months_list = df["月份"].to_list()
col2_list = df["2"].to_list()
col3_list = df["3"].to_list()
col4_list = df["4"].to_list()
col5_list = df["5"].to_list()
col6_list = df["6"].to_list()

# 打印出来给同伴看
print("月份列表：", months_list)
print("列2数据:", col2_list)
print("列3数据:", col3_list)
print("列4数据:", col4_list)
print("列5数据:", col5_list)
print("列6数据:", col6_list)