
#%%
from cProfile import label
import numpy as np
from matplotlib import pyplot as plt
from pyparsing import line
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

#print(mPeaks, mTroughs)

#plot the series with its peaks and troughs and their regression lines, add a legend as well

plt.axline((0,bPeaks), slope = mPeaks, color='blue', linestyle="dashed", label = "Peaks Linear Regression")
plt.axline((0,bTroughs), slope = mTroughs, color='orange', linestyle="dashed", label = "Troughs Linear Regression")
plt.plot(series, color="gray", label="Pricing Data")
plt.plot(peaks, series[peaks], "o", color= "green", label= "Peaks")
plt.plot(troughs, series[troughs], "x",color='red', label = "Troughs")
plt.legend()
plt.show()

# %%
def regress_from_optimum (data: np.ndarray, optimum: np.ndarray) -> (int, int):

    # Regress Optimum Function - Performs linear regression on last peak or trough.
    
    # Parameters**
    
    # Pricing data, 
    # Peak/trough indexing number
    
    # Returns - Slope, y-intercept
 
    opt = optimum[-1]
    data = np.array(data[opt:]).reshape(-1,1)
    x_axis = np.array([i + opt for i in range(len(data))]).reshape(-1,1)
    model = LinearRegression(fit_intercept=True).fit(x_axis,data)
    b = model.intercept_
    m = model.coef_
    return m ,b

def regress_mid(data: np.ndarray, peak: np.ndarray, trough: np.ndarray, lb:int) -> (int,int):

    # Regress Mid Function - Performs linear regression on the peaks and troughs of a given pricing data and calculates a middle line.

    # Parameters**

    # Pricing data,
    # Peak indexing np.number
    # trough indexing number
    # The number of peak/trough points to be used.

    # Returns - Slope, y-intercept
    m1, b1 = regress_optima(series,peaks,lb)
    m2, b2 = regress_optima(series,troughs,lb)

    m = (m1+m2)/2
    b = (b1+b2)/2

    # print (m1, m2)
    # print (b1,b2)

    return m, b
#Call regress_mid on both peaks and troughs
midM, midB = regress_mid(series,peaks,troughs,len(troughs))

#Plot the series with its peaks and troughs as well as your generated mid line
plt.axline((0,bPeaks),slope = mPeaks, color='blue', linestyle = 'dashed', label = 'Peaks Linear Regression')
plt.axline((0,bTroughs), slope = mTroughs, color='orange', linestyle = 'dashed', label = "Troughs Linear Regression")
plt.axline((0,midB), slope=midM, color='black', linestyle='dashed', label = 'Middle Linear Regression')
plt.plot(series, color="gray", label="Pricing Data")
plt.plot(peaks, series[peaks], "o", color='green', label='Peaks')
plt.plot(troughs, series[troughs], "x", color='red', label='Troughs')
plt.legend()
plt.show()

 # %%
def bullish(data: np.ndarray, peak: np.ndarray, trough: np.ndarray, X) -> bool:
    m_peaks, b_peaks = regress_optima(series,peaks,len(peaks))
    m_troughs, b_troughs = regress_optima(series, troughs, len(troughs))

    # if the regression channel is negative don't trade
    if (m_peaks < 0 ) and (m_troughs < 0):
        return False
    # if the regression channel is positive look for more criteria
    elif (m_peaks > 0 ) and (m_troughs > 0):
        #if X is in troughs and the next candle is recovering from the dip --> Buy
        if X in troughs and series[X]< series [X+1]:
            return True
        # if X is in troughs and price action is still falling wait.
       # elif X in troughs and series [X] > series[X+1]:
        #    return False
        #if price is greater than the peaks regression line wait
        elif series[X] > (m_peaks*series[X] + b_peaks):
            return False
        elif series [X] < (m_troughs * series[X] + b_troughs):
            return True
    else:
        return False
    
# %%

#loop through our x axis to feed Bullish every data point to check Conditions.
# Append all true outputs to BUY to later plot on a chart

counter = np.array(range(0,1000)).reshape(-1,1)
tt = np.ndarray(counter.shape, bool)
buy = []
for i in list(counter):
    tt[i] = bullish(series,peaks,troughs,i)
for j in list(counter):
    if tt[j] != False:
        buy.append(j)

#plotting the outputs of my bullish function
plt.plot(series, color = 'orange')
plt.plot(buy,series[buy], 'x', color = 'green', label = "buy signal")
plt.legend()
plt.show()


