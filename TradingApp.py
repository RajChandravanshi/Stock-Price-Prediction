import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon="chart_with_downwards_trend",
    layout='wide'
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide the greatest platform for you to collect all information prior to investing in stocks.")


st.image("trading.jpg")

st.markdown("## We provide the following services:")

st.markdown("### :one: Stock Information")
st.write("Through this page, you can view comprehensive information about individual stocks.")

st.markdown("### :two: Stock Prediction")
st.write("Explore predicted closing prices for the next 30 days based on historical data and advanced forecasting models.")


