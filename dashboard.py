import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set the dark theme
st.set_page_config(layout="wide", page_title="NIFTY 100 ESG Dashboard", page_icon=":chart_with_upwards_trend:")

# Header
st.title('NIFTY 100 ESG Stock Market Dashboard :chart_with_upwards_trend:')

# Sidebar for navigation
st.sidebar.title("Navigation")
sections = ["NIFTY Energy Index Overview", "Historical Stock Data Table", "Live News Section", "NIFTY Energy Performance Table", "Opening Price Prediction", "Company Weightage in NSE Heatmap", "Buying & Selling Decision"]
selected_section = st.sidebar.radio("Go to", sections)

# Load the CSV file
url = 'https://raw.githubusercontent.com/RachitCEH/BFM/main/nifty_100_esg_data.csv'
data = pd.read_csv(url)
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# NIFTY Energy Index Overview
if selected_section == "NIFTY Energy Index Overview":
    st.header("NIFTY Energy Index Overview")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Open'))
    fig.update_layout(title='Open Prices vs Date', xaxis_title='Date', yaxis_title='Open Price', template='plotly_dark')
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig)
    with col2:
        st.write("Date of Inception: 1st April 2004")
        st.write("Base Value: 1000")
        st.write("Major Constituents: Reliance Industries, ONGC, NTPC, Power Grid, Tata Power")

# Historical Stock Data Table
elif selected_section == "Historical Stock Data Table":
    st.header("Historical Stock Data Table")
    years = pd.DatetimeIndex(data['Date']).year.unique()
    selected_year = st.selectbox('Select a Year', years)
    filtered_data = data[data['Date'].dt.year == selected_year]
    st.dataframe(filtered_data[['Date', 'Open', 'Close', 'High', 'Low']])

# Live News Section
elif selected_section == "Live News Section":
    st.header("Live News Section")
    st.write("Fetching live news...")  # Placeholder for live news API integration

# NIFTY Energy Performance Table
elif selected_section == "NIFTY Energy Performance Table":
    st.header("NIFTY Energy Performance Table")
    performance_data = {
        "Sector": ["Renewable Energy", "Oil & Gas", "Power"],
        "Percentage Change": [5.2, 3.8, 4.5]
    }
    performance_df = pd.DataFrame(performance_data)
    st.table(performance_df)

# Opening Price Prediction
elif selected_section == "Opening Price Prediction":
    st.header("Opening Price Prediction")
    st.write("Current Stock Price of Adani Green Energy: ₹1200")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Actual Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'] * 1.01, mode='lines', name='Predicted Open'))  # Example prediction
    fig.update_layout(title='Predicted vs Actual Opening Prices', xaxis_title='Date', yaxis_title='Open Price', template='plotly_dark')
    st.plotly_chart(fig)
    st.write("Error Percentage: 1%")

# Company Weightage in NSE Heatmap
elif selected_section == "Company Weightage in NSE Heatmap":
    st.header("Company Weightage in NSE Heatmap")
    heatmap_data = {
        "Company": ["Reliance Industries", "ONGC", "NTPC", "Power Grid", "Tata Power", "Adani Green Energy", "BPCL", "GAIL", "IOC", "JSW Energy"],
        "Weightage": [20, 15, 12, 10, 8, 7, 6, 5, 4, 3]
    }
    heatmap_df = pd.DataFrame(heatmap_data)
    fig = px.density_heatmap(heatmap_df, x="Company", y="Weightage", color_continuous_scale="Viridis", template="plotly_dark")
    st.plotly_chart(fig)

# Buying & Selling Decision
elif selected_section == "Buying & Selling Decision":
    st.header("Buying & Selling Decision")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Stock Price'))
    fig.update_layout(title='Stock Price Movement', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
    st.plotly_chart(fig)

# Footer
st.sidebar.write("Last Update: 2025-02-09 12:40:21")
st.sidebar.write("Data Source: NIFTY 100 ESG Data CSV")
