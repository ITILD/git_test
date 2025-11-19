from fastapi import FastAPI
import polars as pl
import datetime as dt
from sklearn.linear_model import LinearRegression
from typing import TypeVar,Generic,Union
# 线性回归预测案例
# 导入相关方法
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from pydantic import BaseModel
app=FastAPI()
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
y_new=int(y_new)
print(f"插值后的值为: {y_new}")
# 主函数
def main():
    f,Ar=read_and_process_excel("temp/西红柿.xlsx")
    print(f'f的值为{f}\nAr的值为{Ar}')
    
#读取excel表格中的数据并以列表形式返回每一列的数据
def read_and_process_excel(file_path: str):
    df = pl.read_excel(file_path)
    result = df.to_dict()
    f = result['f'].to_list()
    Ar = result['Ar'].to_list()
    return f,Ar
class Item(BaseModel):
    y_new:int
T=TypeVar("T")
class SuccessResponse(BaseModel,Generic[T]):   #成功  Generic像一个万能模具，可以插入不同模版0
    status:str="success"  #状态码
    data:T #泛型，data:T就是占位符，具体什么类型在使用时决定
class ErrorResponse(BaseModel):
    status:str="error"  #状态码
    message:str #泛型
    code:int
@app.get("/items/{item_id}",response_model=Union[SuccessResponse[Item],ErrorResponse])
async def get_items_model3(item_id:int):
    global y_new
    if item_id==y_new:
#定义要返回的数据
        item=Item(y_new=y_new)
        return SuccessResponse[Item](data=item)
    else:
        return ErrorResponse(message="Item没有找到",code=500)
    
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8000,reload=True)