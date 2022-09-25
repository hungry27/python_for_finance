#region imports
from AlgorithmImports import *
#endregion
from datetime import timedelta
from collections import Counter
class FatFluorescentYellowGuanaco(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2022, 1, 3)  # Set Start Date
        self.SetEndDate(2022, 3,4)
        self.SetCash(100000000)  # Set Strategy Cash
        #self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        #RSI definitions
        RSI_Period    = 14                # RSI Look back period 
        self.RSI_OB   = 75                # RSI Overbought level
        self.RSI_OS   = 25                # RSI Oversold level
        
        self.Equities = ["NVDA","TSLA", "NIO", "AMD","AA"]
        self.Indicators = {}
        self.Charts = {}
        self.Consolidators = {}
        self.prevMacd = {}
        self.prevMacdSignal = {}
        self.psarWin = {}
        self.closeWin = {}
        self.prevRoc = {}
        self.min={}
        self.max={}
        
        # Add equities to portfolio with Hourly Resolution
        for equity in self.Equities:
            self.Consolidators[equity] = {}
            self.AddEquity(equity, Resolution.Hour)
            #self.AddCrypto("BTCUSD", Resolution.Hour, Market.GDAX)
            #self.AddCrypto("ETHUSD", Resolution.Hour, Market.GDAX)
            self.Consolidators[equity]['W1 Con'] = TradeBarConsolidator(timedelta(days=5))
            self.Consolidators[equity]['W1 Con'].DataConsolidated += self.On_W1
            
            #Initializing Indicators
            self.Indicators[equity] = dict()
            self.Indicators[equity]['RSI'] = dict()
            self.Indicators[equity]['RSI']['D'] = self.RSI(equity, RSI_Period)
            self.Indicators[equity]['RSI']['W'] = RelativeStrengthIndex(equity, RSI_Period)
            self.Indicators[equity]['MACD'] = dict()
            self.Indicators[equity]['MACD']['D'] = self.MACD(equity, 12, 26, 9, Resolution.Daily)
            self.Indicators[equity]['PSAR'] = dict()
            self.Indicators[equity]['PSAR']['D'] = self.PSAR(equity, 0.02, 0.02, 0.2, Resolution.Daily)
            self.RegisterIndicator(equity,self.Indicators[equity]['PSAR']['D'], Resolution.Daily)
            self.Indicators[equity]['ROC'] = self.ROC(equity, 14, Resolution.Daily)
            
            self.psarWin[equity] = RollingWindow[IndicatorDataPoint](2)
            self.closeWin[equity] = RollingWindow[TradeBar](3) 
            
            #Previous macd initialization
            self.prevMacd[equity] = None
            self.prevMacdSignal[equity] = None
            self.prevRoc[equity] = None
            self.max[equity] = None
            self.min[equity] = None
            self.PlotIndicator(str(equity) + " MACD", True, self.Indicators[equity]['MACD']['D'], self.Indicators[equity]['MACD']['D'].Signal)
            
            
            self.RegisterIndicator(equity, self.Indicators[equity]['RSI']['W'], self.Consolidators[equity]['W1 Con'])
            #self.RegisterIndicator(equity, self.Indicators[equity]['MACD']['W'], self.Consolidators[equity]['W1 Con'])
            self.SubscriptionManager.AddConsolidator(equity, self.Consolidators[equity]['W1 Con'])
            
            # RSIChartName = equity +"RSI"
            # self.Charts[equity]['RSI'] = Chart(RSIChartName, ChartType.Stacked)
            # self.Charts[equity]['RSI'].AddSeries(Series("D1", SeriesType.Line))
            # self.Charts[equity]['RSI'].AddSeries(Series("W1", SeriesType.Line))
            # self.AddChart(self.Charts[equity]['RSI'])
        
        #Warm up
        self.SetWarmUp(RSI_Period*5)
        
        #create Bullishness Flags
        self.macdBullishness = 0
        self.rsiBullishness = 0
        self.psarBullishness = 0
        self.rocBullishness = 0
        
        #Long and Short indicator lists
        self.macdLongSecurities = []
        self.macdShortSecurities = []
        self.rsiLongSecurities = []
        self.rsiShortSecurities = []
        self.psarLongSecurities = []
        self.psarShortSecurities = []
        
        self.prevLongs = []
        self.prevShorts = []

    #weekly consolidator candles
    def On_W1(self,sender,bar):
        # Make sure we are not warming up 
        if self.IsWarmingUp: return
        Symbol = str(bar.get_Symbol())
        self.Plot(Symbol+'RSI', 'W1', self.Indicators[Symbol]['RSI']['W'].Current.Value)
        
        
    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
        
        bullishnessChange = 0
        
        for equity in self.Equities:
            
            
            noPrevFlag = 0
            
            #Check to see we triggered none action flag
            if self.prevMacd[equity] is None:
                noPrevFlag = 1
                self.prevMacd[equity] = self.Indicators[equity]['MACD']['D'].Current.Value
                self.prevMacdSignal[equity] = self.Indicators[equity]['MACD']['D'].Signal.Current.Value
                continue
            if noPrevFlag == 1:
                return
            
            if not self.Indicators[equity]['PSAR']['D'].IsReady: return
        
            #call and use bullishness functions
            self.macdCheck(equity)
            #self.rsiCheck(equity)
            #self.psarCheck(equity)
            
            #Collect lists of which stocks we are bullish and bearish on
            if self.macdBullishness == 1:
                if equity not in self.macdLongSecurities:
                    bullishnessChange = 1
                    self.macdLongSecurities.append(equity)
                if equity in self.macdShortSecurities:
                    bullishnessChange = 1
                    self.macdShortSecurities.remove(equity)
                
            elif self.macdBullishness == -1:
                if equity not in self.macdShortSecurities:
                    bullishnessChange = 1
                    self.macdShortSecurities.append(equity)
                if equity in self.macdLongSecurities:
                    bullishnessChange = 1
                    self.macdLongSecurities.remove(equity)

            if self.rsiBullishness == 1:
                if equity not in self.rsiLongSecurities:
                    bullishnessChange = 1
                    self.rsiLongSecurities.append(equity)
                if equity in self.rsiShortSecurities:
                    bullishnessChange = 1
                    self.rsiShortSecurities.remove(equity)
                
            elif self.rsiBullishness == -1:
                if equity not in self.rsiShortSecurities:
                    bullishnessChange = 1
                    self.rsiShortSecurities.append(equity)
                if equity in self.rsiLongSecurities:
                    bullishnessChange = 1
                    self.rsiLongSecurities.remove(equity)
                    
            if self.psarBullishness == 1:
                if equity not in self.psarLongSecurities:
                    bullishnessChange = 1
                    self.psarLongSecurities.append(equity)
                if equity in self.psarShortSecurities:
                    bullishnessChange = 1
                    self.psarShortSecurities.remove(equity)
                
            elif self.psarBullishness == -1:
                if equity not in self.psarShortSecurities:
                    bullishnessChange = 1
                    self.psarShortSecurities.append(equity)
                if equity in self.psarLongSecurities:
                    bullishnessChange = 1
                    self.psarLongSecurities.remove(equity)
            
            self.prevMacd[equity] = self.Indicators[equity]['MACD']['D'].Current.Value
            self.prevMacdSignal[equity] = self.Indicators[equity]['MACD']['D'].Signal.Current.Value
            

        #Now that we know which stocks we're bullish on, lets make some trades
        if bullishnessChange == 1:
            longSecurities = self.macdLongSecurities
            shortSecurities = self.macdShortSecurities
            
            for equity in longSecurities:
                if equity in self.rsiLongSecurities:
                    longSecurities.append(equity)
                if equity in self.psarLongSecurities:
                    longSecurities.append(equity)
            
            for equity in shortSecurities:
                if equity in self.rsiShortSecurities:
                    shortSecurities.append(equity)
                if equity in self.psarShortSecurities:
                    shortSecurities.append(equity)

            proportionalLongSecurities = Counter(longSecurities)
            proportionalShortSecurities = Counter(shortSecurities)
            
            longPieSize = len(longSecurities)
            shortPieSize = len(shortSecurities)
            
            if longSecurities != []:
                longBuys = [PortfolioTarget(i, proportionalLongSecurities[i]/longPieSize) for i in proportionalLongSecurities]
                self.Log("Long Buys")
                self.Log(longBuys)
            else:
                longBuys = []
            
            if shortSecurities != []:
                shortSells = [PortfolioTarget(i, -proportionalShortSecurities[i]/shortPieSize) for i in proportionalShortSecurities]
            else:
                shortSells = []
            
            order = shortSells + longBuys
            if order != []:
                self.SetHoldings(order)
            else:
                self.Liquidate()
        
            self.prevLongs = longSecurities
            self.prevShorts = shortSecurities


    #check for buy/sell signal and adjust bullishness flag 
    def macdCheck (self, equity):
        
        if self.Indicators[equity]['MACD']['D'].Current.Value < 0 and self.prevMacd[equity] > 0:
            self.macdBullishness = -1
        elif self.Indicators[equity]['MACD']['D'].Current.Value > 0 and self.prevMacd[equity] < 0:
            self.macdBullishness = 1
        elif self.prevMacd[equity] < self.prevMacdSignal[equity] and self.Indicators[equity]['MACD']['D'].Current.Value > self.Indicators[equity]['MACD']['D'].Signal.Current.Value:
            self.macdBullishness = 1
        elif self.prevMacd[equity] > self.prevMacdSignal[equity] and self.Indicators[equity]['MACD']['D'].Current.Value < self.Indicators[equity]['MACD']['D'].Signal.Current.Value:
            self.macdBullishness = -1
        else:
            self.macdBullishness = 0
         
    #RSI bullish conditions check   
    def rsiCheck (self,equity):
        
        D1_RSI = self.Indicators[equity]['RSI']['D'].Current.Value
        W1_RSI = self.Indicators[equity]['RSI']['W'].Current.Value
        
        Long_Cond1 = D1_RSI < self.RSI_OS
        Long_Cond2 = W1_RSI < self.RSI_OS
        Exit_Cond1 = D1_RSI > self.RSI_OB
        Exit_Cond2 = W1_RSI > self.RSI_OB  
        
        if (Long_Cond1 and Long_Cond2) == True:
            # Buy!
            self.rsiBullishness = 1
            
        elif (Long_Cond1 == True and Long_Cond2 == False):
            self.rsiBullishness = 1
            
        if (Exit_Cond1 and Exit_Cond2) == True:
            # Sell!
            self.rsiBullishness = -1
            
        elif (Exit_Cond1 == True and Exit_Cond2 == False):
            self.rsiBullishness = -1
            
        else:
            self.rsiBullishness = 0
    
    def psarCheck(self, equity):
        
        if not (self.closeWin[equity].IsReady and self.psarWin[equity].IsReady): return
        
        price = self.Securities[equity].Close
        
        self.closeWin[equity].Add(data[equity])
        
        #initialize bar window values
        currBar = self.closeWin[equity][0]
        pastBar = self.closeWin[equity][1]
        
        #initialize. psar window
        currPsar = self.psarWin[equity][0]
        pastPsar = self.psarWin[equity][1]
        
        
        # self.Plot("Trade Plot", "PSAR", self.psar.Current.Value)
        # self.Plot("Trade Plot", "Price", price)
        
        #short if opening PAR is in a downtrend
        if not self.Portfolio.Invested and self.Indicators[equity]['PSAR']['D'].Current.Value > currBar.Close:
            self.psarBullishness = -1
            #self.Plot("Trade Plot", "Sell", price)
            
        #Long if opening PAR is in a uptrend
        elif not self.Portfolio.Invested and self.Indicators[equity]['PSAR']['D'].Current.Value < currBar.Close:
            self.psarBullishness = 1
            #self.Plot("Trade Plot", "Buy", price)
        
        #If previoulsy Bearish and SAR flips to Bullish ---> Long   
        elif pastPsar.Value > pastBar.Close and self.Indicators[equity]['PSAR']['D'].Current.Value < currBar.Close:
            self.psarBullishness = 1
            #self.Plot("Trade Plot", "Buy", price)
        
        #If previously Bullish and SAR flips to bearish ----> Short    
        elif pastPsar.Value < pastBar.Close and self.Indicators[equity]['PSAR']['D'].Current.Value > currBar.Close:
            self.psarBullishness = -1
            #self.Plot("Trade Plot", "Sell", price)
        
        else:
            self.psarBullishness = 0