import datetime
import dateutil.relativedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from finta import TA 
from dateutil.relativedelta import relativedelta

# Fix for compatibility with libraries using 'npNaN'
npNaN = np.nan



def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ["<b>" + str(col)[:15] + "</b>" for col in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[[str(i) for i in dataframe.index]] + [dataframe[col].tolist() for col in dataframe.columns],
            fill_color=[[rowEvenColor, rowOddColor] * (len(dataframe) // 2 + 1)] * (len(dataframe.columns) + 1),
            line_color='lightgrey',
            align='center',
            font=dict(color='black', size=12),
            height=30
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
    return fig


def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months = -1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days = -5)
    
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months = -6)

    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years = -1)

    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years = -5)

    elif num_period == 'ytd':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta('%y-%m-%d')

    else :
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=None):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    # Add Open
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode="lines",
        name='Open',
        line=dict(width=2, color='#5ab7ff')
    ))

    # Add Close
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode="lines",
        name='Close',
        line=dict(width=2, color='black')
    ))

    # Add High
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode="lines",
        name='High',
        line=dict(width=2, color='#0078bf')
    ))

    # Add Low
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode="lines",
        name='Low',
        line=dict(width=2, color='red')
    ))

    # Update axes and layout
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='green',
        legend=dict(
            yanchor='top',
            xanchor='right'
        )
    )

    return fig


def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x = dataframe['Date'], open = dataframe['Open'],
                                 high = dataframe['High'], low = dataframe['Low'],
                                 close = dataframe['Close']))
    
    fig.update_layout(showlegend = False, height = 500, margin = dict(l = 0, r = 20, t = 20, b = 0), plot_bgcolor = 'white', paper_bgcolor = 'green', legend = 
                      dict(yanchor = 'top',
                           xanchor = 'right'))
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = TA.RSI(dataframe)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe.RSI, name = 'RSI', marker_color = 'orange',
                             line = dict(width = 2, color = 'orange'),
                             ))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = [70] * len(dataframe), name = 'Overbought', marker_color = 'red',
                             line = dict(width = 2, color = 'red'),
                             ))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = [30] *len(dataframe),fill = 'tonexty', name = 'Oversold', marker_color = 'orange',
                             line = dict(width = 2, color = 'orange'),
                             ))
    fig.update_layout(yaxis_range = [0,100],
                      height = 200, plot_bgcolor = 'white', paper_bgcolor = 'blue',
                      margin = dict(l = 0 , r = 0, t = 0, b = 0),
                      legend = dict(orientation = 'h', yanchor = 'top',y = 1.02,
                                    xanchor = 'right', x = 1))
    return fig

def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = TA.SMA(dataframe, 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['Open'], mode = 'lines',name = 'Open',
                             line = dict(width = 2, color = 'orange')))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['Close'],mode = 'lines', name = 'Close',
                             line = dict(width = 2, color = 'red')))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['Low'],mode = "lines", name = 'Low',
                             line = dict(width = 2, color = 'orange')))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['High'], mode = 'lines',name = 'High',
                             line = dict(width = 2, color = 'orange'),
                             ))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['SMA_50'], mode = 'lines',name = 'SMA_50',
                             line = dict(width = 2, color = 'orange'),
                             ))
    fig.update_xaxes(rangeslider_visible = True)
    fig.update_layout(height = 200, plot_bgcolor = 'white', paper_bgcolor = '#e1efff',
                      margin = dict(l = 0 , r = 0, t = 0, b = 0),
                      legend = dict(orientation = 'h', yanchor = 'top',
                                    xanchor = 'right'))
    return fig

def MACD(dataframe, num_period):
    macd_df = TA.MACD(dataframe)
    dataframe['MACD'] = macd_df['MACD']
    dataframe['MACD Signal'] = macd_df['SIGNAL']
    macd_hist = dataframe['MACD'] - dataframe['MACD Signal']
    dataframe['MACD Hist'] = dataframe['MACD'] - dataframe['MACD Signal']
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['MACD'], name = 'MACD',marker_color = 'orange',
                             line = dict(width = 2, color = 'orange')))
    fig.add_trace(go.Scatter(x = dataframe['Date'], y = dataframe['MACD Signal'], name = 'MACD Signal', marker_color = 'red',
                             line = dict(width = 2, color = 'red')))
    c = ['red' if cl<0 else 'green' for cl in macd_hist]
    fig.update_layout(yaxis_range = [0,100],
                      height = 200, plot_bgcolor = 'white', paper_bgcolor = '#e1efff',
                      margin = dict(l = 0 , r = 0, t = 0, b = 0),
                      legend = dict(orientation = 'h', yanchor = 'top',y = 1.02,
                                    xanchor = 'right', x = 1))
    return fig


def Moving_average_forecast(forecast):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                            mode = 'lines',
                            name = "Closed Price",
                            line=dict(width=2, color='black')))

    fig.add_trace(go.Scatter(x = forecast.index[-31:], y = forecast['Close'].iloc[-31:],
                             mode = 'lines',
                             name = "Closed Price",
                             line = dict(width = 2, color = 'red')))
    fig.update_xaxes(rangeslider_visible = True)
    fig.update_layout(height = 500, margin = dict(l = 0, r = 20, t = 20, b = 0), plot_bgcolor = 'white', paper_bgcolor = "green",
                      legend = dict(yanchor = 'top',
                                    xanchor = 'right'))
    
    return fig