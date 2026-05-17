import polars as pl

# 读取同文件夹下的Excel
df = pl.read_excel("temp\测试数据.xlsx")

# 打印出来看
print("读取成功！")
print(df)