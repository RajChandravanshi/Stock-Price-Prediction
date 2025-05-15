import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from utils.plotly_figure import plotly_table, filter_data, close_chart, candlestick, RSI, Moving_average, MACD

# Set up the page
st.set_page_config(
    page_title="Stock Analysis",
    page_icon=":page_with_curl:",
    layout='wide'
)

st.title("📈 Stock Analysis App")

# Layout with 3 columns
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

# Date input for selecting date range
with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", today - datetime.timedelta(days=365))
with col3:
    end_date = st.date_input("Choose End Date", today)

st.subheader(ticker)
stock = yf.Ticker(ticker)

# Handle missing keys safely with .get()
st.write(stock.info.get("longBusinessSummary", "No company summary available."))
st.write("**Sector:**", stock.info.get("sector", "N/A"))
st.write("**Full Time Employees:**", stock.info.get("fullTimeEmployees", "N/A"))
st.write("**Website Link:**", stock.info.get("website", "N/A"))


col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=["Market Capital", 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [
        stock.info.get('marketCap', 'N/A'),
        stock.info.get('beta', 'N/A'),
        stock.info.get('trailingEps', 'N/A'), 
        stock.info.get('trailingPE', 'N/A')
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share', 'Profit Margin', 'Debt to Equity', 'Return on Equity'])
    df['Value'] = [
    stock.info.get('quickRatio', 'N/A'),
    stock.info.get('revenuePerShare', 'N/A'),
    stock.info.get('profitMargin','N/A'),
    stock.info.get('debtToEquity', 'N/A'),
    stock.info.get('returnOnEquity', 'N/A')
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

data = yf.download(ticker, start = start_date, end = end_date)
col1, col2, col3 = st.columns(3)

# Check for sufficient rows
if len(data) >= 2:
    last_close = float(data['Close'].iloc[-1])
    prev_close = float(data['Close'].iloc[-2])
    daily_change = last_close - prev_close
    pct_change = (daily_change / prev_close) * 100

    col1.metric(
        label="**Daily Change**",
        value=f"${last_close:.2f}",
        delta=f"{daily_change:+.2f} ({pct_change:+.2f}%)"
    )
else:
    col1.write("Not enough data for daily change.")

last_10_df = data.tail(10).sort_index(ascending = False).round(3)
fig_10 = plotly_table(last_10_df )

st.write("#### Historical Data (Last 10 Days)")
st.plotly_chart(fig_10, use_container_width=True)

st.markdown("### Select the period")
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,1,1,1,1,1,1,1])


num_period = ''
with col1:
    if st.button("5D"):
        num_period = '5D'

with col2:
    if st.button("1M"):
        num_period = '1mo'

with col3:
    if st.button("6M"):
        num_period = '6mo'

with col4:
    if st.button("1Y"):
        num_period = '1y'

with col5:
    if st.button("5Y"):
        num_period = '5y'

with col6:
    if st.button("MAX"):
        num_period = 'max'

col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox("",('Candle', "Line"))
with col2:
    if chart_type == 'Candle':
        indicators  = st.selectbox('',['RSI', "MACD"])
    else:
        indicators = st.selectbox("",("RSI", "Moving Average", 'MACD'))


ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max')
data1 = ticker_.history(period = 'max')

if num_period == '':
    if chart_type == 'Candle' and indicators == "RSI":
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
    
    elif chart_type == 'Candle' and indicators == "MACD":
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    elif chart_type == 'Line' and indicators == "RSI":
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    elif chart_type == 'Line' and indicators == "MACD":
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    elif chart_type == 'Line' and indicators == "Moving Average":
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)
        
    
else:
    if chart_type == 'Candle' and indicators == "RSI":
        st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)
    
    elif chart_type == 'Candle' and indicators == "MACD":
        st.plotly_chart(candlestick(data1, num_period), use_container_width=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True)

    elif chart_type == 'Line' and indicators == "RSI":
        st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)

    elif chart_type == 'Line' and indicators == "MACD":
        st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True)

    elif chart_type == 'Line' and indicators == "Moving Average":
        st.plotly_chart(Moving_average(data1, num_period), use_container_width=True)

