import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
from datetime import datetime
import time

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
margin: 10px 0;  # Reduced margin to decrease gaps between elements
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
    "HDFC Bank": "HDFC Bank is one of India's leading private sector banks, providing a wide range of financial services. "
                 "Founded in 1994, the bank has rapidly grown to become one of the largest and most trusted financial institutions in India. "
                 "HDFC Bank offers a comprehensive suite of banking and financial services, including retail banking, wholesale banking, and treasury operations. "
                 "The bank is known for its strong emphasis on customer service, innovative products, and extensive branch network.",
    
    "Infosys": "Infosys is a global leader in technology services and consulting, enabling clients in more than 50 countries. "
               "Founded in 1981, Infosys has become a pioneer in the IT services industry, offering a wide range of services including application development, cloud computing, data analytics, and digital transformation. "
               "The company is renowned for its commitment to innovation, sustainability, and corporate social responsibility. "
               "With a strong focus on employee development and cutting-edge technology, Infosys continues to drive growth and deliver exceptional value to its clients.",
    
    "Larsen & Toubro": "Larsen & Toubro is an Indian multinational engaged in technology, engineering, construction, manufacturing, and financial services. "
                       "Established in 1938, L&T has grown into a conglomerate with a presence in over 30 countries. "
                       "The company is known for its expertise in executing large and complex projects across various sectors, including infrastructure, power, defense, and aerospace. "
                       "L&T's commitment to quality, innovation, and sustainability has earned it a reputation as one of the most respected and reliable companies in India and beyond.",
    
    "Tata Consultancy Services": "Tata Consultancy Services is a global leader in IT services, consulting, and business solutions. "
                                 "Founded in 1968, TCS is part of the Tata Group, India's largest industrial conglomerate. "
                                 "The company offers a comprehensive range of services, including software development, business process outsourcing, and IT infrastructure management. "
                                 "TCS is known for its customer-centric approach, innovative solutions, and strong focus on sustainability and corporate governance. "
                                 "With a presence in over 46 countries, TCS continues to drive digital transformation for businesses worldwide.",
    
    "Reliance Industries": "Reliance Industries is a conglomerate holding company headquartered in Mumbai, India, engaged in diverse businesses. "
                           "Founded in 1966, Reliance has grown to become one of the largest and most profitable companies in India. "
                           "The company's business interests span across petrochemicals, refining, oil and gas exploration, retail, telecommunications, and digital services. "
                           "Reliance is known for its relentless pursuit of growth and innovation, making significant investments in technology and sustainable practices. "
                           "With a strong focus on customer satisfaction and operational excellence, Reliance continues to set new benchmarks in the Indian business landscape.",
    
    "Wipro": "Wipro is a leading global information technology, consulting, and business process services company. "
             "Established in 1945, Wipro has evolved from a vegetable oil manufacturer to a global IT services powerhouse. "
             "The company offers a wide range of services, including IT consulting, application development, cloud computing, and cybersecurity. "
             "Wipro is recognized for its commitment to innovation, sustainability, and social responsibility. "
             "With a strong focus on employee development and cutting-edge technology, Wipro continues to drive growth and deliver exceptional value to its clients."
}

# Display the dynamic description in the second column
with col2:
    st.write("### ABOUT COMPANY")
    st.write(company_descriptions[selected_company])

# New Features

# Live News Ticker
st.header("Live Market Updates")
news_api_key = "ZRF0P3GRP8P9078H"
response = requests.get(f"https://newsapi.org/v2/everything?q=NIFTY%20100%20ESG&apiKey={news_api_key}")
news_data = response.json()

# Check if the articles key exists in the response
if 'articles' in news_data:
    news_headlines = "\n".join([f"{article['publishedAt']} - {article['title']}" for article in news_data['articles']])
    st.text(news_headlines)
else:
    st.text("No news articles found or error in fetching data.")

# Real-Time Stock Price Table using Alpha Vantage API
st.header("Real-Time Stock Price Table")

# Function to fetch live data from Alpha Vantage
def fetch_alpha_vantage_data():
    API_KEY = "ZRF0P3GRP8P9078H"  # Replace with your Alpha Vantage API key
    symbol = "NSE:NIFTY100ESG"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (5min)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (5min)"], orient="index")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
    else:
        return None

# Display live data from Alpha Vantage
alpha_vantage_data = fetch_alpha_vantage_data()
if alpha_vantage_data is not None:
    st.write(alpha_vantage_data.head())
else:
    st.write("Error fetching data from Alpha Vantage")

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
st.cache_data.clear()
time.sleep(30)
st.experimental_rerun()
