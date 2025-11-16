
import polars as pl
import datetime as dt
from sklearn.linear_model import LinearRegression

def linear_regression_prediction():

    arr1=[1,2,3,4,5]
    arr2=[13,12,20,30,31]



def main():
    ex_1=read_and_process_excel("temp/西红柿.xlsx")


def read_and_process_excel(file_path: str) -> pl.DataFrame:
    df = pl.read_excel(file_path)
    result = df.to_dicts()
    return result

if __name__ == "__main__":
    main()







