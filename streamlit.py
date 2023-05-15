import streamlit as st
import pandas as pd

import base64
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
    selected_tag = st.selectbox \
        ("Select a tag", ["a", "b", "c", "d", "e"], key = row,)
    #
    # # Store the selected tag in the tagged_data dataframe
    tagged_data.at[index, "tag"] = selected_tag

# Display the tagged dataframe
st.subheader("Tagged Dataset")
st.dataframe(tagged_data)


csv = tagged_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="tagged_data.csv">Download CSV</a>'
st.markdown(href, unsafe_allow_html=True)
