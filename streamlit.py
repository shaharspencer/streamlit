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
    username = st.selectbox("Select User", valid_users, format_func=lambda user: f"👤 {user}", key=0)
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
        st.write(f"**Sentence {index+1}:** {sentence}")
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"], key=row)
        # Perform any necessary processing or storage of the tag

# Main app
def main():
    st.title("Multiple User Streamlit App")

    if 'user' not in st.session_state or st.session_state.user is None:
        login()
    else:
        user = st.session_state.user

        if user == "Shahar":
            st.title("Shahar's Page")
            st.write("Welcome to Shahar's section!")
            dataframe_shahar = pd.DataFrame({"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})
            tag_sentences(dataframe_shahar)
        elif user == "Gabi":
            st.title("Gabi's Page")
            st.write("Welcome to Gabi's section!")
            dataframe_gabi = pd.DataFrame({"sentence": ["Sentence A", "Sentence B", "Sentence C"]})
            tag_sentences(dataframe_gabi)
        elif user == "Ittamar":
            st.title("Ittamar's Page")
            st.write("Welcome to Ittamar's section!")
            dataframe_ittamar = pd.DataFrame({"sentence": ["Example 1", "Example 2", "Example 3"]})
            tag_sentences(dataframe_ittamar)
        elif user == "Nurit":
            st.title("Nurit's Page")
            st.write("Welcome to Nurit's section!")
            dataframe_nurit = pd.DataFrame({"sentence": ["Text 1", "Text 2", "Text 3"]})
            tag_sentences(dataframe_nurit)

        # Add a logout button in the sidebar
        st.sidebar.button("Logout", on_click=logout)

# Run the app
if __name__ == '__main__':
    main()
