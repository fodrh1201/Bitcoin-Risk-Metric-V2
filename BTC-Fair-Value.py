from sklearn import linear_model
import pandas as pd
import numpy as np
import quandl as quandl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mplcursors as mplcursors
import ccxt


### Import historical bitcoin price from quandl
# df = quandl.get("BCHAIN/MKPRU", api_key="FYzyusVT61Y4w65nFESX").reset_index()
# df["Date"] = pd.to_datetime(df["Date"])
# df.sort_values(by="Date", inplace=True)
# df = df[df["Value"] > 0]
binance = ccxt.binance()
df = quandl.get('BCHAIN/MKPRU', api_key='FYzyusVT61Y4w65nFESX').reset_index()
df['Date'] = pd.to_datetime(df['Date'])
ohlcv = binance.fetch_ohlcv('BTC/USDT', timeframe='1d')
ohlcv_df = pd.DataFrame(ohlcv, columns=['Date', 'OPEN', 'HIGH', 'LOW', 'Value', 'Volume'])
timestamp_240108= binance.parse8601('2024-01-08T00:00:00')
ohlcv_df = ohlcv_df[ohlcv_df['Date'] > timestamp_240108]

ohlcv_df['Date'] = pd.to_datetime(ohlcv_df['Date'], unit='ms')
ohlcv_df = ohlcv_df[['Date', 'Value']]
df.sort_values(by='Date', inplace=True)
df = pd.concat([df, ohlcv_df]).reset_index().iloc[:-1][['Date', 'Value']]
df = df[df['Value'] > 0]

### RANSAC Regression
def LinearReg(ind, value):
    X = np.array(np.log(ind)).reshape(-1, 1)
    y = np.array(np.log(value))
    ransac = linear_model.RANSACRegressor(residual_threshold=2.989, random_state=0)
    ransac.fit(X, y)
    LinearRegRANSAC = ransac.predict(X)
    return LinearRegRANSAC
print(df.index)
df["LinearRegRANSAC"] = LinearReg(df.index, df.Value)

#### Plot
fig = make_subplots()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], name="Price", line=dict(color="gold")))
fig.add_trace(go.Scatter(x=df["Date"], y=np.exp(df["LinearRegRANSAC"]), name="Ransac", line=dict(color="green")))
fig.update_layout(template="plotly_dark")
mplcursors.cursor(hover=True)
fig.update_xaxes(title="Date")
fig.update_yaxes(title="Price", type='log', showgrid=True)
fig.show()
