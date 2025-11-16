
import polars as pl
import datetime as dt
from sklearn.linear_model import LinearRegression

# 线性回归预测案例
# 导入相关方法
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
# 生成随机回归训练数据集，有100个实列即100行
X, y = make_regression(n_samples=100, n_features=2, noise=0.1, random_state=1)
# 拟合模型
model = LinearRegression()
model.fit(X, y)

# 生成新的预测集，有3个实例即3行
Xnew, _ = make_regression(n_samples=3, n_features=2, noise=0.1, random_state=1)
# 开始预测
ynew = model.predict(Xnew)
# 展示预测的值
print('预测值：')
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))
# 展示真实的值
print('真实值：')
for i in range(len(Xnew)):
	print("X=%s, Real=%s" % (Xnew[i], _[i]))

# 创建一维插值模型
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

def main():
    ex_1=read_and_process_excel("temp/西红柿.xlsx")
    print(ex_1)
    

def read_and_process_excel(file_path: str) -> pl.DataFrame:
    df = pl.read_excel(file_path)
    result = df.to_dicts()
    return result

if __name__ == "__main__":
    main()







