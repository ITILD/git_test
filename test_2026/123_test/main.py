import pandas as pd

# 1. 替换这里的路径
# 注意：路径前面要加字母 r，或者把 \ 全部改成 /
# 例如：r'C:\Users\你的名字\Desktop\test.xlsx'
file_path = r'C:\Users\Lenovo\Documents\xwechat_files\wxid_hr9iwrc6flk622_d892\msg\file\2026-03\1.xlsx'

# 2. 读取文件
try:
    df = pd.read_excel(file_path)
    print("读取成功！前5行数据如下：")
    print(df.head())
except FileNotFoundError:
    print("错误：找不到文件，请检查路径是否拼写正确。")