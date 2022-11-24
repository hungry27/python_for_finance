import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas_datareader import data as pdr

# import data
def get_data(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start, end)
    stockData = stockData['Close']
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix

stockList = ['AAPL' , 'META', 'MSFT', 'AMD', 'CSCO', 'SNAP']
# stocks = [stock + '.AX' for stock in stockList]
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 300)

meanReturns, covMatrix = get_data(stockList,startDate, endDate)

weights = np.random.random(len(meanReturns))
weights = weights/np.sum(weights)

# print(weights)

# print(meanReturns)

#Monte Carlo Method
# Number of simulations
mc_sims = 100
T = 100 #timeframe in days

MeanM = np.full(shape=(T,len(weights)), fill_value = meanReturns)
meanM = MeanM.T

portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)


initialPortfolio = 10000

#Monte Carlo loops
for m in range(0, mc_sims):
    #MC loops
    Z = np.random.normal(size=(T, len(weights)))
    L = np.linalg.cholesky(covMatrix)
    dailyReturns = meanM + np.inner(L,Z)
    portfolio_sims[:,m] = np.cumprod(np.inner(weights,dailyReturns.T)+1)*initialPortfolio


#Value at risk
def mcVaR(returns, alpha = 5):
    """
    Input: Pandas series of returns
    Output: Percentile on return distribution to a given confidence level alpha
    """
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected a pandas data series")

#Conditional Value at risk
def mcCVaR(returns, alpha = 5):
    """
    Input: Pandas series of returns
    Output: CVaR or Expected Shortfall to a given confidence level alpha
    """
    if isinstance(returns, pd.Series):
        belowVar = returns <= mcVaR(returns, alpha = alpha)
        return returns[belowVar].mean()
    else:
        raise TypeError("Expected a pandas data series")

# Portfolio Results
portResults = pd.Series(portfolio_sims[-1,:])

#Value at Risk
VaR = initialPortfolio - mcVaR(portResults, alpha=5)

#Consitional Value at risk
CVaR = initialPortfolio - mcCVaR(portResults, alpha=5)

print('VaR ${}'.format(round(VaR,2)))
print('CVaR ${}'.format(round(CVaR,2)))

plt.plot(portfolio_sims)
plt.ylabel('Portfolio Value ($)')
plt.xlabel('Days')
plt.title('MC Simulation of stock portfolio')
plt.axhline(y=VaR, color='r', linestyle='-')
plt.axhline(y=CVaR, color='b', linestyle='-')
plt.show()
