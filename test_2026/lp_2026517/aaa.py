import polars as pl
def read():
    path_self="temp/test(1).xlsx"
    df = pl.read_excel(path_self)
    print(df)
    
 # 修复列名（解决Series name报错）
    df.columns = [str(col) for col in df.columns]

# #  处理数据（示例：新增一行）
# new_row = pl.DataFrame({
#     "1": [10],
#     "2": [11],
#     "3": [13],
#     "4": [],
#     "5": [20],
#     "6": [25]
# })
# df_updated = pl.concat([df, new_row])

# # 3. 写回原Excel，覆盖Sheet1
# df_updated.write_excel(
#     "temp/test(1).xlsx",
#     engine="openpyxl",
#     sheet_name="Sheet1",
#     overwrite=True,
#     column_widths="auto"
# )
# print(df_updated)

if __name__ == "__main__":   
    path_self="temp/test(1).xlsx"
    data:list =read(path_self)