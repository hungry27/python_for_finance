import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression

x = (np.random.rand(1000)*np.random.randn(1000) + 0.5)*np.diff(np.random.randn(1001))

series = np.cumsum(x)
series += 300
y = series
plt.plot(series)