import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned merged file from Google Drive
file_url = 'https://drive.google.com/uc?id=1N1khETHukgorjixdrC0Pe_x2U3j5a_ce'  # Direct download link
merged_data = pd.read_csv(file_url)

# Prepare the data
merged_data['Invoice Date'] = pd.to_datetime(merged_data['Invoice Date'], errors='coerce')
merged_data.set_index('Invoice Date', inplace=True)

# Calculate Revenue (Quantity * Price)
merged_data['Revenue'] = merged_data['Quantity'] * merged_data['Price']

# Group by week and sum the quantities sold
weekly_sales = merged_data.resample('W')['Quantity'].sum()

# Identify the top 10 stock codes based on total quantity sold
top_stock_codes = merged_data.groupby('Stock Code')['Quantity'].sum().nlargest(10).index.tolist()

# Identify the top 10 high revenue products
top_revenue_products = merged_data.groupby('Stock Code')['Revenue'].sum().nlargest(10).index.tolist()

# Streamlit app layout
st.title("Demand Forecasting Dashboard")

# Sidebar for selecting stock code from Top 10 Stock Codes or Top 10 Revenue Products
selected_stock_code = st.sidebar.selectbox("Select Stock Code:", 
                                             top_stock_codes + top_revenue_products)

# Determine the category of the selected stock code
if selected_stock_code in top_stock_codes:
    category = "Top 10 Quantity"
else:
    category = "Top 10 Revenue"

# Display summary metrics for selected stock code
stock_data = merged_data[merged_data['Stock Code'] == selected_stock_code]
total_sales = stock_data['Quantity'].sum()
average_sales = stock_data['Quantity'].mean()
total_revenue = stock_data['Revenue'].sum()

st.metric("Total Sales", f"{total_sales:.0f}")
st.metric("Average Weekly Sales", f"{average_sales:.0f}")
st.metric("Total Revenue", f"${total_revenue:.2f}")

if selected_stock_code:
    # Fit ARIMA model for the selected stock code
    stock_weekly_sales = stock_data.resample('W')['Quantity'].sum()
    
    # Split the data into train and test sets
    train_size = int(len(stock_weekly_sales) * 0.8)
    train, test = stock_weekly_sales[:train_size], stock_weekly_sales[train_size:]

    model = ARIMA(train, order=(5, 1, 0))  # Adjust order as needed
    model_fit = model.fit()

    # Forecast the next 15 weeks
    forecast = model_fit.forecast(steps=len(test))
    forecast_index = pd.date_range(start=train.index[-1] + pd.Timedelta(weeks=1), periods=len(test), freq='W')
    forecast_series = pd.Series(forecast, index=forecast_index)

    # Calculate errors
    errors = test - forecast_series
    training_errors = train - model_fit.fittedvalues[:train_size]

    # Display forecast results
    st.write(f"Forecast for Stock Code: {selected_stock_code}")
    st.line_chart(forecast_series)

    # Plot training and testing error distribution
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))

    # Training Error Distribution
    sns.histplot(training_errors, kde=True, ax=axs[0])
    axs[0].set_title('Training Error Distribution')
    axs[0].set_xlabel('Error')
    axs[0].set_ylabel('Frequency')

    # Testing Error Distribution
    sns.histplot(errors, kde=True, ax=axs[1])
    axs[1].set_title('Testing Error Distribution')
    axs[1].set_xlabel('Error')
    axs[1].set_ylabel('Frequency')

    st.pyplot(fig)

st.write("Note: Ensure the stock code exists in the dataset.")
