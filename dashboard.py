import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
from datetime import datetime
import time

st.title("Live Market Updates & Performance Metrics - NIFTY 100 ESG Index")

# Real-Time Market Updates
st.header("Real-Time Market Updates")
news_api_key = "YOUR_NEWS_API_KEY"
response = requests.get(f"https://newsapi.org/v2/everything?q=NIFTY%20100%20ESG&apiKey={news_api_key}")
news_data = response.json()
for article in news_data['articles']:
    st.write(f"{article['publishedAt']} - {article['title']}")

# Live Price & Performance Metrics
st.header("Live Price & Performance Metrics")
nifty_data = yf.download("^NSEI", period="1d", interval="1m")
percentage_change = ((nifty_data['Close'][-1] - nifty_data['Open'][0]) / nifty_data['Open'][0]) * 100
status = "🔼" if percentage_change > 0 else "🔻"
st.metric(label="NIFTY 100 ESG Index", value=nifty_data['Close'][-1], delta=f"{percentage_change:.2f}% {status}")

# Sector-Wise Performance Heatmap
st.header("Sector-Wise Performance Heatmap")
sector_data = pd.DataFrame({ # Example data, replace with actual sector data
    "Sector": ["Tech", "Finance", "Healthcare", "Energy", "Consumer"],
    "Performance": [1.5, -0.5, 2.0, -1.0, 0.5]
})
heatmap = go.Figure(data=go.Heatmap(z=sector_data["Performance"], x=sector_data["Sector"], colorscale='Viridis'))
st.plotly_chart(heatmap, use_container_width=True)

# Top Gainers & Losers Table
st.header("Top Gainers & Losers")
# Example data, replace with actual data
data = {
    "Stock Name": ["Stock A", "Stock B", "Stock C", "Stock D"],
    "Current Price": [100, 200, 150, 250],
    "% Change (24h)": [5, -3, 2, -4],
    "Volume": [1000, 1500, 1200, 1800],
    "Market Cap": [5000, 10000, 7500, 12500]
}
df = pd.DataFrame(data)
st.table(df)

# Real-Time Data Refresh
if st.button("Refresh Data"):
    st.experimental_rerun()

# Auto-refresh every 30 seconds
st.experimental_singleton.clear()
time.sleep(30)
st.experimental_rerun()
