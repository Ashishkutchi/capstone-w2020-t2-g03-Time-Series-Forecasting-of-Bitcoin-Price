#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install --upgrade plotly
pip install numpy
pip install pystan

# In[2]:


import datetime
from binance.client import Client
import pandas as pd
from fbprophet import Prophet
import numpy as np


# In[3]:


client = Client('5oJKxLS9xif8zp5bbsjRr67s5h4oWvmCh3D6ZOlbdFNwYDvDkLNXPLfyVjJ53vUT','kxpoCJI9la6MQTOJlJzgNLPy4X4XdRlNkX8QmZJCjPnPDf9vgu3ib46x1veWv9fU')


# In[4]:


symbol = 'BTCUSDT'
BTC = client.get_historical_klines(symbol=symbol, interval = Client.KLINE_INTERVAL_1DAY  , start_str = '1 year ago UTC')
# See Binance API support doc > Binance Constants for intervals and 
# See Binance API support doc >MArket Data Endpoints > Aggregate Trade Iterator for start_str examples
# KLINE_INTERVAL_1DAY
# KLINE_INTERVAL_30MINUTE


# In[ ]:





# In[ ]:





# In[5]:


# See Binance API support doc > Binance API > client module for column names
BTC = pd.DataFrame(BTC, columns=['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','ignored'])


# In[6]:


BTC['Open time'] = pd.to_datetime(BTC['Open time'], unit='ms')


# In[ ]:





# In[7]:


df_new=BTC[['Open time','Close']]


# In[ ]:





# In[8]:


df_new=df_new.rename(columns={'Open time':'ds','Close':'y'})


# In[9]:


df_new['y'] = df_new['y'].astype(float)


# In[10]:


df_old = df_new.copy()


# In[11]:


df_old.head()


# In[12]:


df_new['y'] = np.log(df_new['y'])


# In[13]:


m=Prophet(interval_width=0.95, yearly_seasonality=True, weekly_seasonality=True,daily_seasonality=True, changepoint_prior_scale=2)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5, prior_scale=0.02)
m.fit(df_new)
future = m.make_future_dataframe(periods = 365,freq='D')


# In[14]:


forecast = m.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


# In[15]:


all_pred = forecast[['ds','yhat']]


# In[16]:


all_pred['yhat'] = np.exp(all_pred['yhat'])


# In[17]:


all_pred.set_index('ds',inplace=True)


# In[18]:


all_pred.loc['2020-02-20']


# In[19]:


df_old.set_index('ds',inplace=True)


# In[20]:


df_old.loc['2020-02-20']


# In[ ]:




