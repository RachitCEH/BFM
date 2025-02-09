import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests
import numpy as np

# Load the CSV file from the repository
url = 'https://raw.githubusercontent.com/RachitCEH/BFM/main/nifty_100_esg_data.csv'
data = pd.read_csv(url)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Create a line chart
fig = go.Figure()

fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Open'))

# Update layout of the chart
fig.update_layout(title='Open Prices vs Date',
                  xaxis_title='Date',
                  yaxis_title='Open Price',
                  template='plotly_dark')

# Display the chart in Streamlit
st.plotly_chart(fig)
