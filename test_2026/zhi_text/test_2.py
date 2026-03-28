# 拉取Excel表格并进行增删
import pandas as pd

# 读取Excel文件
df = pd.read_excel("你的Excel文件路径.xlsx")

# 增加数据
new_row = {"列名1": "值1", "列名2": "值2"}
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# 删除数据（例如删除某列值为指定内容的行）
df = df[df["列名"] != "要删除的值"]

# 保存修改后的Excel文件
df.to_excel("修改后的Excel文件路径.xlsx", index=False)