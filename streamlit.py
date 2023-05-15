import streamlit as st
import pandas as pd

# Define the list of valid users
valid_users = ["Shahar", "Gabi", "Ittamar", "Nurit"]


# User authentication
def authenticate(username):
    # Check if the provided username is in the list of valid users
    if username in valid_users:
        return True
    else:
        return False


# Login form
def login():
    username = st.selectbox("Select User", valid_users,
                            format_func=lambda user: f"👤 {user}")
    if st.button("Login"):
        if authenticate(username):
            # Store the authenticated user in session state
            st.session_state.user = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username")


# Logout button
def logout():
    if st.button("Logout"):
        # Clear the session state user
        st.session_state.user = None
        st.success("Logged out")


# Function to tag sentences
def tag_sentences(dataframe):
    st.title("Tag Sentences")
    st.write("Tag sentences with options 'a', 'b', 'c', 'd', 'e'")
    for index, row in dataframe.iterrows():
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"])
        # Perform any necessary processing or storage of the tag


# Main app - Shahar section
def shahar_page():
    st.title("Shahar's Page")
    st.write("Welcome to Shahar's section!")
    # Load or generate a dataframe for Shahar
    dataframe_shahar = pd.DataFrame(
        {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})
    # Call the tagging function for Shahar
    tag_sentences(dataframe_shahar)


# Main app - Gabi section
def gabi_page():
    st.title("Gabi's Page")
    st.write("Welcome to Gabi's section!")
    # Load or generate a dataframe for Gabi
    dataframe_gabi = pd.DataFrame(
        {"sentence": ["Sentence A", "Sentence B", "Sentence C"]})
    # Call the tagging function for Gabi
    tag_sentences(dataframe_gabi)


# Main app - Ittamar section
def ittamar_page():
    st.title("Ittamar's Page")
    st.write("Welcome to Ittamar's section!")
    # Load or generate a dataframe for Ittamar
    dataframe_ittamar = pd.DataFrame(
        {"sentence": ["Example 1", "Example 2", "Example 3"]})
    # Call the tagging function for Ittamar
    tag_sentences(dataframe_ittamar)


# Main app - Nurit section
def nurit_page():
    st.title("Nurit's Page")
    st.write("Welcome to Nurit's section!")
    # Load or generate a dataframe for Nurit
    dataframe_nurit = pd.DataFrame(
        {"sentence": ["Text 1", "Text 2", "Text 3"]})
    # Call the tagging function for Nurit
    tag_sentences(dataframe_nurit)


# Main app
def main():
    st.title("Multiple User Streamlit App")

    if 'user' not in st.session_state or st.session_state.user is None:
        pass

