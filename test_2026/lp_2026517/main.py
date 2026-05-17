import numpy as np
import polars as pl
from scipy.interpolate import CubicSpline
from chazhi import data
from aaa import read
from aaa import write

def main():
    print("Hello from lp-2026517!")

if __name__ == "__main__":  
    input_path = "temp/test(1).xlsx"
    x_known, y_known, missing = read(input_path)

    # 2. 构建完整月份列表并插值
    all_months = sorted(x_known + missing)   # 例如 [1,2,3,4,5,6]
    all_values = []
    for m in all_months:
        if m in x_known:
            idx = x_known.index(m)
            all_values.append(y_known[idx])
        else:
            val = data(x_known, y_known, m)   # 已经是 float
            all_values.append(val)

    # 3. 写回原文件（或另存为新文件）
    output_path = input_path   # 覆盖原文件
    # 若想保留原文件，可改为 output_path = "temp/test_filled.xlsx"
    write(output_path, all_months, all_values)
    print(f"插值完成，文件已保存至：{output_path}")
