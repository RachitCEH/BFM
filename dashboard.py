import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# Set custom background image for the dashboard
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
background: url("https://raw.githubusercontent.com/RachitCEH/BFM/main/abstract-futuristic-technology-blank-wallpaper-free-vector.jpg");
background-size: cover;
}
[data-testid="stMarkdownContainer"] {
background-color: #2d2e81;  # Background color
color: white;  # White font color
padding: 20px;  # Padding inside the text box
margin: 20px;  # Margin around the text box
border-radius: 10px;  # Rounded corners
}
[data-testid="stVerticalBlock"] > div {
margin: 20px 0;  # Add margin to the text elements
}
h1, h3 {
text-align: center;  # Center align the header and subheaders
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Add the header for the entire dashboard
st.title("NIFTY 100 ESG DASHBOARD")

# List of companies
companies = ["HDFC Bank", "Infosys", "Larsen & Toubro", "Tata Consultancy Services", "Reliance Industries", "Wipro"]

# Function to get stock data
@st.cache_data
def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

# Function to calculate moving averages
def add_moving_averages(df, windows=[20, 50, 100]):
    for window in windows:
        df[f'MA{window}'] = df['Close'].rolling(window=window).mean()
    return df

# Function to get support levels
def get_support_levels(df):
    levels = []
    for i in range(2, len(df) - 2):
        if df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] and df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]:
            levels.append((i, df['Low'][i]))
    return levels

# Create a dropdown for company selection below the line chart section
selected_company = st.selectbox('Select a Company', companies)

# User input for timeframe
timeframe = st.selectbox('Select Timeframe', ['1mo', '3mo', '6mo', '1y', '2y', '5y'])

# Load stock data
ticker_map = {
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "Larsen & Toubro": "LT.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Reliance Industries": "RELIANCE.NS",
    "Wipro": "WIPRO.NS"
}
data = get_stock_data(ticker_map[selected_company], period=timeframe)

# Add moving averages to the data
data = add_moving_averages(data)

# Get support levels
support_levels = get_support_levels(data)

# Create a line chart
fig = go.Figure()

# Add the main line for stock prices
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close', line=dict(color='#FFFFFF')))

# Add moving averages to the chart
for window in [20, 50, 100]:
    fig.add_trace(go.Scatter(x=data.index, y=data[f'MA{window}'], mode='lines', name=f'MA{window}', line=dict(dash='dash')))

# Add support levels to the chart
for level in support_levels:
    fig.add_shape(type='line', x0=data.index[level[0]], y0=level[1], x1=data.index[level[0] + 1], y1=level[1], line=dict(color='Red',))

# Update layout of the chart
fig.update_layout(title=f'{selected_company} - Stock Price Trend',
                  xaxis_title='Date',
                  yaxis_title='Close Price',
                  plot_bgcolor='#2d2e81',  # Set background color to the same color
                  template='plotly_dark')

# Create two equal-sized columns for the chart and the description
col1, col2 = st.columns([2, 1])

# Display the chart in the first column
with col1:
    st.write(f"### {selected_company} - Stock Price Trend")
    st.plotly_chart(fig, use_container_width=True)

# Display the NIFTY 100 ESG description in the second column
with col2:
    st.write("### NIFTY 100 ESG")
    st.write("""
    The NIFTY 100 ESG Index is designed to reflect the performance of companies within the NIFTY 100 index that meet certain environmental, social, and governance (ESG) criteria. 
    The index includes companies that are leaders in ESG practices while also considering their financial performance. 
    It aims to provide investors with an ESG-compliant benchmark that represents the top 100 companies in India. 
    This allows investors to make more informed decisions.
    
    By integrating ESG criteria, the index promotes sustainable and responsible investment practices.
    """)

# Display the selected company name on the dashboard
st.write(f"Selected Company: {selected_company}")
