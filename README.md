📊 Demand Forecasting Dashboard
A comprehensive Demand Forecasting tool that predicts future product sales using time series forecasting techniques. This dashboard allows users to explore top-selling products and visualize demand predictions, helping businesses make informed inventory and sales decisions.

🔍 Project Overview
This project focuses on building a Streamlit-based dashboard for predicting product demand using ARIMA models. We utilized historical sales data, cleaned and merged it, and applied time series forecasting to predict future demand for top-selling products.

Key Features:
📈 ARIMA Time Series Forecasting for weekly demand prediction.
🏆 Top Products: Identify the top 10 products based on total sales quantity and total revenue.
📊 Interactive Visualizations for sales trends, demand forecasts, and error distributions.
🖥️ Deployed on Streamlit Cloud for easy accessibility.
🚀 Live Demo
Check out the live app here----https://my-demand-forecasting-app.streamlit.app/

📂 Dataset
The dataset used in this project consists of cleaned and merged sales transaction data, which includes:

Invoice: Unique invoice identifier
Stock Code: Product identifier
Quantity: Number of units sold
Price: Unit price of the product
Customer ID: Unique customer identifier
Invoice Date: Date of the transaction
Revenue: Calculated as Quantity * Price
The file is hosted on Google Drive due to size constraints and loaded directly into the app.

⚙️ How It Works
Data Preparation:
Cleaned and merged multiple raw datasets.
Calculated total revenue for each transaction.
Aggregated weekly sales for time series analysis.
Time Series Forecasting:

Applied ARIMA model to forecast future sales based on historical data.
Split data into training and test sets (80/20 split) for evaluation.
Streamlit Dashboard:

Users can interactively select products from the top 10 by sales quantity or revenue.
Display key metrics: Total sales, average weekly sales, and total revenue.
Visualize future demand forecasts along with training and testing error distributions.
