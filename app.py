import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

@st.cache_data  # Use st.cache_data for caching data-related functions
def load_data(ticker):
    """Function for loading data"""
    # Fetch data for the selected ticker
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")

    # Separate numeric and text columns
    numeric_df = df.select_dtypes(['float', 'int'])
    numeric_cols = numeric_df.columns

    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns

    return df, numeric_cols, text_cols

# Define some example tickers (you may customize this list)
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "JNJ", "JPM", "V", "PG", 
    "WMT", "KO", "INTC", "NFLX", "HD", "PYPL", "CMCSA", "PEP", "ADBE", "CSCO", 
    "MRK", "UNH", "XOM", "NKE", "PFE", "VZ", "INTU", "ABBV", "SBUX", "ABT", 
    "TXN", "IBM", "MDT", "AVGO", "CVX", "GILD", "LMT", "BAC", "ORCL", "DHR", 
    "NOW", "AMGN", "MMM", "SPOT", "ZM", "CRM", "GOOG", "F", "GM", "BA", "DIS"
]
  # Example tickers

# Get the unique tickers
unique_stocks = list(set(tickers))

# Select a stock
selected_ticker = st.selectbox("Select a stock", unique_stocks)

# Load data for the selected stock
df, numeric_cols, text_cols = load_data(selected_ticker)

# Title of dashboard
st.title("Stock Dashboard")

# Add checkbox to sidebar
check_box = st.sidebar.checkbox(label="Display dataset")

if check_box:
    # Show the dataset
    st.write(df)

# Give sidebar a title
st.sidebar.title("Settings")
st.sidebar.subheader("Timeseries settings")
feature_selection = st.sidebar.multiselect(label="Features to plot",
                                           options=numeric_cols)

# Filter data for the selected features
df_features = df[feature_selection]

# Plot the selected features
if not df_features.empty and feature_selection:
    plotly_figure = px.line(
        data_frame=df,
        x=df.index,
        y=feature_selection,
        title=f'{selected_ticker} timeline'
    )

    st.plotly_chart(plotly_figure)
else:
    st.write("Please select at least one feature to plot.")
