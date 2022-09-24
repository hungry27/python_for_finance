
#%%
from cProfile import label
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression

#Setting up random data for testing
x = (np.random.rand(1000)*np.random.randn(1000) + 0.5)*np.diff(np.random.randn(1001))
series = np.cumsum(x)
series += 300
y = series
plt.plot(series)

# %%

#Find the peaks of the dummy data
peaks, _ = find_peaks(series, distance = 50)
#list containing the height of the peaks

plt.plot(series)
plt.plot(peaks, series[peaks], "x")
#Plot the dummy data and its peaks
plt.show()

#Find the troughs of the dummy data
find_troughs = lambda series: find_peaks(-series, distance = 50 )
troughs, _ = find_troughs(series)
plt.plot(series)
plt.plot(troughs, series[troughs], "o")
#Plot the dummy data and its troughs
plt.show()
# %%

def regress_optima(data: np.ndarray, optima: np.ndarray, lb: int) -> (int,int):

# Regress Optima Function - Performs linear regression on peaks and troughs of a given pricing data

# Parameters**

# Pricing data,
# Peak/trough indexing number
# The number of peak/trough points to be used.

# Returns - Slope, y-intercept

    temp = [data[opt] for opt in optima[-lb:]]
    model = LinearRegression(fit_intercept=True).fit(optima[-lb:, np.newaxis],temp)
    b = model.intercept_
    m = model.coef_

    return m, b

#Call regression optima on both the peaks array and troughs array
mPeaks, bPeaks = regress_optima(series,peaks,len(peaks))
mTroughs, bTroughs = regress_optima(series, troughs, len(troughs))

print(mPeaks, mTroughs)

#plot the series with its peaks and troughs and their regression lines, add a legend as well

plt.axline((0,bPeaks), slope = mPeaks, color='blue', linestyle="dashed", label = "Peaks Linear Regression")
plt.axline((0,bTroughs), slope = mTroughs, color='orange', linestyle="dashed", label = "Troughs Linear Regression")
plt.plot(series, color="gray", label="Pricing Data")
plt.plot(peaks, series[peaks], "o", color= "green", label= "Peaks")
plt.plot(troughs, series[troughs], "x",color='red', label = "Troughs")
plt.legend()
plt.show()

# %%
