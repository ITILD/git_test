import numpy as np
import polars as pl
from scipy.interpolate import CubicSpline
from chazhi import data
from aaa import read

def main():
    print("Hello from lp-2026517!")

if __name__ == "__main__":   
    path_self="temp/test(1).xlsx"
    data:list =read(path_self)
    print(data)           
    main()
