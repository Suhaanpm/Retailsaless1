import pandas as pd
import streamlit as st

# Title
st.title("Retail Sales Trend Analysis Dashboard")

# Load data
df = pd.read_csv("retailsalesss.csv", encoding='latin1')

# Cleaning
df = df.loc[:, ~df.columns.str.contains('Unnamed')]
df = df[df['Order ID'].notna()]

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')

df = df.dropna(subset=['Order Date','Sales'])

# Feature Engineering
df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)

# KPI
total_sales = df['Sales'].sum()
total_orders = df['Order ID'].nunique()
avg_order_value = total_sales / total_orders

st.metric("Total Sales", total_sales)
st.metric("Total Orders", total_orders)
st.metric("Avg Order Value", avg_order_value)

# Monthly Trend
monthly_sales = df.groupby('YearMonth')['Sales'].sum().reset_index()
st.line_chart(monthly_sales.set_index('YearMonth'))

# Category Sales
category_sales = df.groupby('Category')['Sales'].sum()
st.bar_chart(category_sales)

# Scatter
st.write("Sales vs Profit")
st.scatter_chart(df[['Sales','Profit']])
