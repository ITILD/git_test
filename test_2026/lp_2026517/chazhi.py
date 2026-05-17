import numpy as np
from scipy.interpolate import CubicSpline

def data(x_known:list, y_known:list, month:int)->float:
    """_summary_

    Args:
        x_known (list): _月份_
        y_known (list): _数据_
        month (int): _未知数据月份_

    Returns:
        int: _未知的数据值_
    """
    x_known_np = np.array(x_known)
    y_known_np = np.array(y_known)
    cs = CubicSpline(x_known_np, y_known_np)
    return float(cs(month))
    
    
if __name__ == "__main__":
    y_full = data([1, 2, 3, 5, 6], [10, 11, 13, 20, 25], 4)
    print(y_full)                   