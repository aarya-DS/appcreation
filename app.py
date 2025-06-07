import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Street Food Explorer", layout="wide")

# Title
st.title("🌮 Street Food Explorer")
st.markdown("Discover global street food trends, pricing, and more.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Street Food Data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Country Filter
countries = df['Country'].dropna().unique().tolist()
selected_countries = st.sidebar.multiselect("Select Country", countries, default=countries)
df = df[df['Country'].isin(selected_countries)]

# Region/City Filter
if 'Region/City' in df.columns:
    regions = df['Region/City'].dropna().unique().tolist()
    selected_regions = st.sidebar.multiselect("Select Region/City", regions, default=regions)
    df = df[df['Region/City'].isin(selected_regions)]

# Vegetarian Filter
if 'Vegetarian' in df.columns:
    vegetarian_options = df['Vegetarian'].dropna().unique().tolist()
    selected_type = st.sidebar.multiselect("Vegetarian?", vegetarian_options, default=vegetarian_options)
    df = df[df['Vegetarian'].isin(selected_type)]

# If no data
if df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# Preview data
st.subheader("📋 Filtered Data Preview")
st.dataframe(df, use_container_width=True)

# Summary
st.subheader("📊 Summary Statistics")
st.write(df[['Typical Price (USD)']].describe())

st.markdown("---")
st.subheader("📈 Visualizations")

# Column layout
col1, col2 = st.columns(2)

# Pie Chart: Vegetarian vs Non-Vegetarian
with col1:
    if 'Vegetarian' in df.columns:
        st.markdown("### 🥗 Vegetarian vs Non-Vegetarian")
        veg_counts = df['Vegetarian'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(veg_counts, labels=veg_counts.index, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)

# Bar Chart: Average Price by Cooking Method
with col2:
    if 'Cooking Method' in df.columns and 'Typical Price (USD)' in df.columns:
        st.markdown("### 🍳 Avg Price by Cooking Method")
        avg_price = df.groupby('Cooking Method')['Typical Price (USD)'].mean().sort_values()
        st.bar_chart(avg_price)

# Bar Chart: Most Common Dishes by Region
if 'Region/City' in df.columns:
    st.markdown("### 🏙️ Dish Count by Region/City")
    region_counts = df['Region/City'].value_counts().head(10)
    st.bar_chart(region_counts)

# Histogram: Price Distribution
st.markdown("### 💸 Price Distribution")
fig2, ax2 = plt.subplots()
ax2.hist(df['Typical Price (USD)'].dropna(), bins=10, color='skyblue', edgecolor='black')
ax2.set_xlabel("Price (USD)")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | by Aarya Kondawar")
