import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# Load the CSV file from the repository
url = 'https://raw.githubusercontent.com/RachitCEH/BFM/main/nifty_100_esg_data.csv'
data = pd.read_csv(url)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Assuming the dominant color from the new image is a shade of blue
dominant_color = '#2d2e81'  # Example dominant color (blue)

# Create a line chart
fig = go.Figure()

fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Open', line=dict(color=dominant_color)))

# Update layout of the chart
fig.update_layout(title='NIFTY 100 NSE - OPEN PRICE TREND',
                  xaxis_title='Date',
                  yaxis_title='Open Price',
                  plot_bgcolor='#2d2e81',  # Set background color to the same color
                  template='plotly_dark')

# Create two equal-sized columns for the chart and the description
col1, col2 = st.columns([2, 1])

# Display the chart in the first column
with col1:
    st.write("### NIFTY 100 NSE - OPEN PRICE TREND")
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

# Create a dropdown for company selection below the line chart section
selected_company = st.selectbox('Select a Company', companies)

# Display the selected company name on the dashboard
st.write(f"Selected Company: {selected_company}")
