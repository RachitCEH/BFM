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

# Create a dropdown for company selection below the line chart section
selected_company = st.selectbox('Select a Company', companies)

# Display the selected company name on the dashboard
st.write(f"Selected Company: {selected_company}")

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

# Create a line chart
fig = go.Figure()

# Add the main line for stock prices
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close', line=dict(color='#FFFFFF')))

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

# Company descriptions
company_descriptions = {
    "HDFC Bank": "HDFC Bank is one of India's leading private sector banks, providing a wide range of financial services.",
    "Infosys": "Infosys is a global leader in technology services and consulting, enabling clients in more than 50 countries.",
    "Larsen & Toubro": "Larsen & Toubro is an Indian multinational engaged in technology, engineering, construction, manufacturing, and financial services.",
    "Tata Consultancy Services": "Tata Consultancy Services is a global leader in IT services, consulting, and business solutions.",
    "Reliance Industries": "Reliance Industries is a conglomerate holding company headquartered in Mumbai, India, engaged in diverse businesses.",
    "Wipro": "Wipro is a leading global information technology, consulting, and business process services company."
}

# Display the dynamic description in the second column
with col2:
    st.write("### ABOUT COMPANY")
    st.write(company_descriptions[selected_company])
