import streamlit as st
import pandas as pd
from streamlit.hashing import _CodeHasher
import base64

# Title of the web app
st.title("Sentence Tagging App")

# Load the dataframe
data = pd.read_csv("your_dataframe.csv")

# Create a unique session ID for each user
session_id = st.report_thread.get_report_ctx().session_id
session_hash = _CodeHasher().hash(session_id)
user_id = session_hash % (10 ** 8)

# Create a copy of the dataframe to store the tagged values
tagged_data = data.copy()

# Check if user tags exist in the session state, initialize if not
if 'user_tags' not in st.session_state:
    st.session_state['user_tags'] = {}

# Iterate over each row in the dataframe
for index, row in tagged_data.iterrows():
    sentence = row["sentence"]

    # Display the sentence
    st.subheader(f"Sentence {index + 1}")
    st.write(sentence)

    # Create a selectbox for tagging options
    selected_tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"])

    # Store the selected tag in the user_tags dictionary
    st.session_state['user_tags'][(user_id, index)] = selected_tag

# Display the tagged dataset
st.subheader("Tagged Dataset")
tagged_data['tag'] = [st.session_state['user_tags'].get((user_id, index)) for index in range(len(tagged_data))]
st.dataframe(tagged_data)

# Download the tagged dataset as a CSV file
csv = tagged_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="tagged_data.csv">Download CSV</a>'
st.markdown(href, unsafe_allow_html=True)
