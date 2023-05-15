import streamlit as st
import numpy as np
import pandas as pd

# Title of the web app
st.title("Dummy Data Streamlit App")

# Create a dummy dataframe
data = pd.DataFrame({
    'Column 1': np.random.randn(100),
    'Column 2': np.random.randint(0, 10, 100),
    'Column 3': np.random.uniform(1.0, 5.0, 100)
})

# Display the dataset
st.subheader("Dummy Dataset")
st.dataframe(data)

# Show descriptive statistics
st.subheader("Descriptive Statistics")
st.write(data.describe())

