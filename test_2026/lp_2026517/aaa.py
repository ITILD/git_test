import polars as pl

def read(path_self: str):
    """
    从 Excel 中提取已知月份、已知数值、缺失月份。
    要求 Excel 结构：
        - 第一行：月份数字（如 1,2,3,4,5,6）
        - 第二行：对应数值（如 10,11,13,空,20,25）
    返回三个列表：
        x_known, y_known, missing_months
    """
    # 读取 Excel，不将第一行作为表头（has_header=False）
    df = pl.read_excel(path_self, has_header=False)

    # 至少需要两行数据
    if df.height < 2:
        raise ValueError("Excel 中至少需要两行：月份行和数值行。")

    month_row = df.row(0)   # 第一行：月份
    value_row = df.row(1)   # 第二行：数值

    x_known = []
    y_known = []
    missing_months = []

    for m, v in zip(month_row, value_row):
        month_int = int(m)          # 确保月份是整数
        if v is not None:
            x_known.append(month_int)
            y_known.append(v)
        else:
            missing_months.append(month_int)

    return x_known, y_known, missing_months
# ========== 主程序 ==========

if __name__ == "__main__":
    path_self = "temp/test(1).xlsx"
    x_known, y_known, missing = read(path_self)

    print(f"已知月份: {x_known}")
    print(f"已知数值: {y_known}")
    print(f"缺失月份: {missing}")