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