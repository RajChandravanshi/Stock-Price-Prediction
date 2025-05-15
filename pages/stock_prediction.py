import streamlit as st
from utils.model_train import *
import pandas as pd
from utils.plotly_figure import *


st.set_page_config(
    page_title="Stock Price Prediction", 
    page_icon="📈",
    layout='wide'
)


st.title("📊 Stock Price Prediction")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("**Stock Ticker**", "TSLA")

rmse = 0
st.subheader(f"Predicting next 30 days Closing price for: **{ticker}**")
data = get_data(ticker)
close_price = data["Close"]

rolling_mean = get_rolling_mean(close_price)
differencing_order = get_differencing_order(close_price)
scaled_data, scaler = scaling(rolling_mean)

rmse = evaluate_model(scaled_data, differencing_order)
st.write("**Model RMSE Score**: ", rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast["Close"] = inverse_scaling(scaler, forecast)
st.write('#### Forecast Data For Next 30 day')
fig_table = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_table.update_layout(height = 220)
st.plotly_chart(fig_table, use_container_width = True)

forecast = pd.concat([rolling_mean, forecast])

st.plotly_chart(Moving_average_forecast(forecast.iloc[-150:]),use_container_width = True)