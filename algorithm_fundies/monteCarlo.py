# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

from sklearn import covariance
from pandas_datareader import data as pdr

# import data
def get_data(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start, end)
    stockData = stockData['Close']
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix

stockList = ['CBA' , 'BHP', 'TLS', 'NAB', 'WBC', 'STO']
stocks = [stock + '.AX' for stock in stockList]
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 300)

meanReturns, covMatrix = get_data(stocks,startDate, endDate)

weights = np.random.random(len(meanReturns))
weights = weights/np.sum(weights)

# print(weights)

# print(meanReturns)

#Monte Carlo Method
# Number of simulations
mc_sims = 500
T = 100 #timeframe in days

MeanM = np.full(shape=(T,len(weights)), fill_value = meanReturns)
meanM = MeanM.T

portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)

# %%

initialPortfolio = 10000



for m in range(0, mc_sims):
    #MC loops
    Z = np.random.normal(size=(T, len(weights)))
    L = np.linalg.cholesky(covMatrix)
    dailyReturns = meanM + np.inner(L,Z)
    portfolio_sims[:,m] = np.cumprod(np.inner(weights,dailyReturns.T)+1)*initialPortfolio

plt.plot(portfolio_sims)
plt.ylabel('Portfolio Value ($)')
plt.xlabel('Days')
plt.title('MC Simulation of stock portfolio')
plt.show()
# %%
