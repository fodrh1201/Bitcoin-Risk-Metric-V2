# %%
from datetime import date
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import quandl
import yfinance as yf
import ccxt
binance = ccxt.binance()
df = quandl.get('BCHAIN/MKPRU', api_key='FYzyusVT61Y4w65nFESX').reset_index()
df['Date'] = pd.to_datetime(df['Date'])
ohlcv = binance.fetch_ohlcv('BTC/USDT', timeframe='1d')
ohlcv_df = pd.DataFrame(ohlcv, columns=['Date', 'OPEN', 'HIGH', 'LOW', 'Value', 'Volume'])
timestamp_240108= binance.parse8601('2024-01-08T00:00:00')
ohlcv_df = ohlcv_df[ohlcv_df['Date'] > timestamp_240108]

ohlcv_df['Date'] = pd.to_datetime(ohlcv_df['Date'], unit='ms')
ohlcv_df = ohlcv_df[['Date', 'Value']]
ohlcv_df
df.sort_values(by='Date', inplace=True)

df = df[df['Value'] > 0]
df = pd.concat([df, ohlcv_df]).reset_index().iloc[:-1][['Date', 'Value']]
# %%
btcdata = yf.download(tickers='BTC-USD', period='1d', interval='1m')

# %%
# Append the latest price data to the dataframe
df.loc[df.index[-1]+1] = [date.today(), btcdata['Close'].iloc[-1]]# %%
# %%
# %%
df