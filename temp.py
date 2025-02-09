import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# List of companies
companies = ["HDFC Bank", "Infosys", "Larsen & Toubro", "Tata Consultancy Services", "Reliance Industries", "Wipro"]

# Create a dropdown for company selection
selected_company = st.selectbox('Select a Company', companies)

# Display the selected company name on the dashboard
st.write(f"Selected Company: {selected_company}")

# Load the CSV file from the repository (example for one company, you can add logic to load specific company data)
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

# Divide the page into two equal-sized columns
col1, col2 = st.columns(2)

# Display the chart in the first column
with col1:
    st.plotly_chart(fig)
