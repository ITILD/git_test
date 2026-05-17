import pandas as pd
import numpy as np

# 创建一个有缺失值的示例数据
df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [10, np.nan, 30, 40, 50]
})

# 用每列的均值填充缺失值
df_filled = df.fillna(df.mean())

print(df_filled)