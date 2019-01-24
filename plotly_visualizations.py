import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
#Global Variables
infile="C:\Users\AM17060\Downloads\Ethereum_ExchangeData.csv"

#Read infile into data frame
df=pd.read_csv(infile,delimiter=",",encoding="utf-8")
# assign columns to variables
date_time=df.start_time
low_price=df.low_price
high_price=df.high_price
open_price=df.open_price
close_price=df.close_price
volume=df.volume

#create derived metrics
price_flux=close_price-open_price


#create datetime object and aggregate at day-level
day=pd.to_datetime(date_time)
grouped_data=df.groupby(by=day,level=None).mean()


#create box plots
trace0=go.Box(
	x=day,
	y=price_flux,
	boxmean=True
)

#create scatter plots

trace1=go.Scatter(
	x=day,
	y=high_price, 
	mode='line',
	name='high price'
)

trace2=go.Scatter(
	x=day,
	y=low_price,
	mode='line',
	name='low price'
)

trace3=go.Scatter(
	x=day,
	y=price_flux,
	name='price variation',
	mode='markers',
	 marker = dict(
        color=[-50,50],
		size='6',
		cmax=40,
		cmin=-40,
		opacity=.75,
        line = dict(width = 1),
        
		)
	
)
#data_box=[trace0]
data_scatter=[trace3]
py.offline.plot(data_scatter,filename='price-flux.html')
#py.offline.plot(data_box,filename='price-flux.html')