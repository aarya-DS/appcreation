import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Street Food Insights App")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Street Food Data.csv")

df = load_data()

# Show dataset
st.subheader("Preview of Street Food Data")
st.dataframe(df)

# Show column names
st.sidebar.title("Filters")

# Example filter: select a city/area if the column exists
if 'Area' in df.columns:
    area = st.sidebar.selectbox("Select Area", df['Area'].dropna().unique())
    filtered_df = df[df['Area'] == area]
else:
    filtered_df = df

# Show some stats
st.subheader("Summary Statistics")
st.write(filtered_df.describe(include='all'))

# Plot example: pie chart of food types or vendors
if 'Food Type' in df.columns:
    st.subheader("Distribution of Food Types")
    food_counts = filtered_df['Food Type'].value_counts()
    st.pyplot(plt.figure(figsize=(6, 6)))
    plt.pie(food_counts, labels=food_counts.index, autopct="%1.1f%%", startangle=140)
    plt.axis('equal')
    plt.title("Food Type Share")

# Add more visualizations as needed

st.markdown("📊 More charts and filters can be added based on your dataset's columns.")
# Bar chart for Vendor Count per Area (if available)
if 'Area' in df.columns and 'Vendor Name' in df.columns:
    st.subheader("Number of Vendors per Area")
    vendor_counts = df.groupby('Area')['Vendor Name'].nunique().sort_values(ascending=False)
    st.bar_chart(vendor_counts)

# Bar chart of Average Price per Food Type (if price column exists)
if 'Food Type' in df.columns and 'Price' in df.columns:
    st.subheader("Average Price per Food Type")
    avg_price = filtered_df.groupby('Food Type')['Price'].mean().sort_values()
    st.bar_chart(avg_price)

# Line chart for items sold per day (if there's a Date and Quantity column)
if 'Date' in df.columns and 'Quantity Sold' in df.columns:
    st.subheader("Quantity Sold Over Time")
    df['Date'] = pd.to_datetime(df['Date'])
    daily_sales = df.groupby('Date')['Quantity Sold'].sum()
    st.line_chart(daily_sales)

# Histogram of Prices
if 'Price' in filtered_df.columns:
    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['Price'].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | By Aarya Kondawar")
