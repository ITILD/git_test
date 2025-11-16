
import polars as pl
import datetime as dt
from sklearn.linear_model import LinearRegression


# 线性回归预测  
def linear_regression_prediction():

    arr1=[1,2,3,4,5]
    arr2=[13,12,20,30,31]



# 创建一维插值模型
def linear_interpolation(x, y):
    f = interp1d(x, y, kind='linear')
    return f
from scipy.interpolate import interp1d
import numpy as np
# 已知数据点
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 2, 4, 6, 8])
# 创建插值函数
f = interp1d(x, y, kind='linear')
# 插值计算
x_new = 2.5
y_new = f(x_new)
print(f"插值后的值为: {y_new}")


# 主函数
def main():
    ex_1=read_and_process_excel("temp/西红柿.xlsx")

# 读取Excel文件并预处理
def read_and_process_excel(file_path: str) -> pl.DataFrame:
    df = pl.read_excel(file_path)
    result = df.to_dicts()
    return result

if __name__ == "__main__":
    main()







