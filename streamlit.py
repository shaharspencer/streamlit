import streamlit as st
import pandas as pd

# Title of the web app
st.title("Sentence Tagging App")

# Load the dataframe
data = pd.read_csv(r"morph_order_by_count_2023_01_15.csv")

# Display the dataframe
st.subheader("Original Dataset")
st.dataframe(data)

# Create a copy of the dataframe to store the tagged values
tagged_data = data.copy()

# Iterate over each row in the dataframe
for index, row in tagged_data.iterrows():
    sentence = row["Sentence"]

    # Display the sentence
    st.subheader(f"Sentence {index + 1}")
    st.write(sentence)

    # # Create a selectbox for tagging options
    selected_tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"])
    #
    # # Store the selected tag in the tagged_data dataframe
    tagged_data.at[index, "tag"] = selected_tag

# Display the tagged dataframe
st.subheader("Tagged Dataset")
st.dataframe(tagged_data)
