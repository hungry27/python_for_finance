
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, CryptoBarsRequest, StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

# no keys required.
crypto_client = CryptoHistoricalDataClient()

# keys required


'''
# multi symbol request - single symbol is similar
multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])

latest_multisymbol_quotes = stock_client.get_stock_latest_quote(multisymbol_request_params)

gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
'''

# no keys required for crypto data
client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD", "ETH/USD"],
                        timeframe=TimeFrame.Hour,
                        start="2022-09-01T00:00:00",
                        end="2022-09-10T00:00:00"
                 )      
crypto_bars = client.get_crypto_bars(request_params)

'''
print(crypto_bars)


stock_request_params=StockBarsRequest(
       symbol_or_symbols=["META"],
       timeframe=TimeFrame.Minute,
       start="2022-09-10T13:00:00",
       end="2022-09-11T14:00:00"
)

stock_bars = stock_client.get_stock_bars(stock_request_params)


print(stock_bars)
'''

def extract_ohlc(bars):

       Date = []
       Open =[]
       Close =[]
       High =[]
       Low =[]
       Volume = []

       for entry in bars["ETH/USD"]:
              Date.append(entry.timestamp)
              Open.append(entry.open)
              Close.append(entry.close)
              High.append(entry.high)
              Low.append(entry.low)
              Volume.append(entry.volume)

       return Date, Open, Close, High, Low, Volume

Date, Open, Close, High, Low, Volume = extract_ohlc(crypto_bars)

df = pd.DataFrame({'date' : Date,
                     'open' : Open,
                     'close' : Close,
                     'high' : High,
                     'low' : Low,
                     'volume' : Volume
})

#print(df)

#Create cashflow column and do an operation to populate it
df["cashflow"] = ((df.high+df.low)/2) * df.volume


#print(df)

#plot the graphs needed. namely OHLC, volume and Cashflow

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03, subplot_titles=('OHLC Eth/Usd','Volume (Units)','Cashflow ($ Millions)'),row_width=[0.2,0.2,0.7])

fig.add_trace(go.Ohlc( x = Date,
                    open = Open,
                    high = High,
                    low = Low,
                    close = Close,
                    name = 'OHLC'),
              row=1, col=1)
fig.add_trace(go.Bar(x=Date,
                     y = df.volume,
                     showlegend=False), row=2, col=1)
fig.add_trace(go.Bar(x=Date,
                     y = df.cashflow,
                     showlegend=False), row=3, col=1)

fig.update(layout_xaxis_rangeslider_visible=False)

fig.show()

