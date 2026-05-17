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


import openpyxl

def write(file_path: str, months: list, values: list):
    """
    将完整的月份和数值写回 Excel 文件（覆盖第一个工作表）。
    格式：第一行月份数字，第二行对应数值。
    使用 openpyxl，无需额外安装 xlsxwriter 或 fastexcel。
    """
    # 尝试打开已有文件（如果存在），否则创建新工作簿
    try:
        wb = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        wb = openpyxl.Workbook()

    # 使用第一个工作表，清空原有内容
    ws = wb.active
    ws.title = "Sheet1"
    ws.delete_rows(1, ws.max_row)
    ws.delete_cols(1, ws.max_column)

    # 写入第一行：月份数字
    for col_idx, month in enumerate(months, start=1):
        ws.cell(row=1, column=col_idx, value=month)

    # 写入第二行：数值
    for col_idx, value in enumerate(values, start=1):
        ws.cell(row=2, column=col_idx, value=value)

    # 自动调整列宽（简单实现）
    for col_cells in ws.columns:
        max_length = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))
        adjusted_width = max_length + 2
        ws.column_dimensions[col_letter].width = adjusted_width

    # 保存文件
    wb.save(file_path)
    
    
if __name__ == "__main__":
    path_self = "temp/test(1).xlsx"
    x_known, y_known, missing = read(path_self)

    print(f"已知月份: {x_known}")
    print(f"已知数值: {y_known}")
    print(f"缺失月份: {missing}")

