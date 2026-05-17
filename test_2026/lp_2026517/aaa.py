import polars as pl
df = pl.read_excel(
    "temp/test(1).xlsx")
print(df)

 # 修复列名（解决Series name报错）
df.columns = [str(col) for col in df.columns]

#  处理数据（示例：新增一行）
new_row = pl.DataFrame({
    "1": [10],
    "2": [11],
    "3": [13],
    "4": [],
    "5": [20],
    "6": [25]
})
df_updated = pl.concat([df, new_row])

# 3. 写回原Excel，覆盖Sheet1
df_updated.write_excel(
    "temp/test(1).xlsx",
    engine="openpyxl",
    sheet_name="Sheet1",
    overwrite=True,
    column_widths="auto"
)
print(df_updated)