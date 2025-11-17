def main():
    # 从Excel文件读取数据的示例
    print("Hello from text-depend!")
import polars as pl
import datetime as dt
import os

def read_excel_data(file_path):
    """从Excel文件读取数据并返回Polars DataFrame"""
    try:
        # 使用Polars的read_excel函数读取Excel文件
        # 注意：需要安装相关依赖，如openpyxl或xlsx2csv
        df = pl.read_excel(file_path)
        return df
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        print("请确保已安装openpyxl或xlsx2csv依赖")
        # 如果读取失败，返回一个示例DataFrame
        return pl.DataFrame(
            {
                "name": ["first month", "second month", "third month", "fourth month"],
                "birthdate": [
                    dt.date(1997, 1, 10),
                    dt.date(1985, 2, 15),
                    dt.date(1983, 3, 22),
                    dt.date(1981, 4, 30),
                ],
                "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
                "height": [1.56, 1.77, 1.65, 1.75],  # (m)
            }
        )

# 示例Excel文件路径（请根据实际情况修改）
# 使用原始字符串避免反斜杠转义问题
excel_file_path = r"C:\Users\28406\Desktop\xiangmu.xlsx"

# 读取Excel数据
df = read_excel_data(excel_file_path)

print("读取的数据:")
print(df)

if __name__ == "__main__":
    main()
