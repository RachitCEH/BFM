import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

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

# Function to fetch live data
def fetch_live_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="1d", interval="1m")  # Fetch live data with 1-minute interval

# Function to get financial data (EPS, PE ratio, IPO price)
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    eps = info.get("trailingEps")
    pe_ratio = info.get("trailingPE")
    ipo_price = None  # Replace with actual IPO price if available
    return eps, pe_ratio, ipo_price

# Function to get historical data for Nifty 100 ESG for the last 5 years
def get_historical_data():
    symbol = "^NSE100ESG"
    stock = yf.Ticker(symbol)
    return stock.history(period="5y")

# Function to read CSV file
@st.cache_data
def load_csv_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)

# Function to load heatmap data
@st.cache_data
def load_heatmap_data(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1')

# Function to generate heatmap
def generate_heatmap(data):
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(data, annot=True, cmap='coolwarm', cbar=True, square=True, linewidths=.5)
    plt.title("TOP 10 Companies in NIFTY 100 ESG")
    st.pyplot(plt)

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
ticker = ticker_map[selected_company]
data = get_stock_data(ticker, period=timeframe)

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
               "Founded in 1981, Infosys has become a pioneer in the IT services industry, offering a wide range of services including application development, cloud computing, data analytics, and more. "
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

# Fetch and display financial data
eps, pe_ratio, ipo_price = get_financial_data(ticker)
st.write(f"### Financial Data for {selected_company}")
st.write(f"**EPS:** {eps}")
st.write(f"**PE Ratio:** {pe_ratio}")
st.write(f"**IPO Price:** {ipo_price if ipo_price else 'N/A'}")

# Fetch and display historical data for Nifty 100 ESG
st.header("Nifty 100 ESG Historical Data (Last 5 Years)")
historical_data = get_historical_data()
st.line_chart(historical_data['Close'])

# Fetch live data for Nifty 100 ESG
nifty100_esg_data = fetch_live_data("^NSE100ESG")

# Display live data
st.header("Nifty 100 ESG Live Data")
st.line_chart(nifty100_esg_data['Close'])

# Load CSV data and display it
csv_data = load_csv_data("nifty_100_esg_data.csv")
st.header("Nifty 100 ESG Data from CSV")

# Create two columns for the CSV data and the graph
col_csv, col_graph = st.columns(2)

with col_csv:
    st.dataframe(csv_data)

# Display line graph using Date vs Open columns from the csv file
with col_graph:
    st.write("### Nifty 100 ESG Historical Data")
    fig_csv = go.Figure()
    csv_data['Date'] = pd.to_datetime(csv_data['Date'], errors='coerce')  # Ensure the Date column is in datetime format
    fig_csv.add_trace(go.Scatter(x=csv_data['Date'], y=csv_data['Open'], mode='lines', name='Open', line=dict(color='#FFFFFF')))
    fig_csv.update_layout(title='Nifty 100 ESG - Date vs Open',
                          xaxis_title='Date',
                          yaxis_title='Open Price',
                          plot_bgcolor='#2d2e81',  # Set background color to the same color
                          template='plotly_dark',
                          xaxis=dict(
                              tickmode='linear',
                              dtick='M12',
                              tickformat='%Y'
                          ))
    st.plotly_chart(fig_csv, use_container_width=True)

# Load heatmap data and generate heatmap
heatmap_data = load_heatmap_data("Heatmap.csv")
st.header("TOP 10 Companies in NIFTY 100 ESG")
generate_heatmap(heatmap_data)
