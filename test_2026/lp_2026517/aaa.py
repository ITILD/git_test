import polars as pl
def read(path_self):
    df = pl.read_excel(path_self,
    has_header=False)
    print(df)
    
 # 修复列名（解决Series name报错）
    # df.columns = [str(col) for col in df.columns]
 # 1. 把整个DataFrame转成 list（二维列表）
    data_list = [list(row) for row in df.rows()]
    print("\n二维列表形式（每行一个子列表）：")
    print(data_list)

    # 其他操作...（修改、写回）
    return  data_list  # 返回list    

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
    print(data)