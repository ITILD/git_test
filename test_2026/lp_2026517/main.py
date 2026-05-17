import numpy as np
import polars as pl
from scipy.interpolate import CubicSpline
from chazhi import data
from aaa import read
from aaa import write

def main():
    print("Hello from lp-2026517!")

if __name__ == "__main__":  
    path_self = "temp/test(1).xlsx"
    x_known, y_known, missing = read(path_self)

   
    y_full = data(x_known, y_known, missing)
    print(y_full)   
     # 2. 模拟插值过程
    all_months = sorted(x_known + missing)
    all_values = []
        
        # 将已知数据转为字典，提高后续查找效率（避免在循环中反复使用 index 查找）
    known_dict = dict(zip(x_known, y_known))
    avg_val = sum(y_known) / len(y_known) # 模拟插值的均值
        
    for m in all_months:
            if m in known_dict:
                val = known_dict[m]  # 已知月份，直接取值
            else:
                val = avg_val        # 缺失月份，填入模拟的插值结果
            all_values.append(val)
        
        # 3. 覆盖写入原表
    write(all_months, all_values, path_self)
                 
    main()
