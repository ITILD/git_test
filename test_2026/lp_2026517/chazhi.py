import numpy as np
from scipy.interpolate import CubicSpline

def data(x_known, y_known, month):
   
    cs = CubicSpline(x_known, y_known)
    return cs(month)
    
    
if __name__ == "__main__":
    x_known = np.array([1, 2, 3, 5, 6])
    y_known = np.array([10, 11, 13, 20, 25])
    x_full = np.arange(1, 7)
    y_full = data(x_known, y_known, x_full)
    print(y_full)                   