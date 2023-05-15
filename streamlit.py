import streamlit as st
import pandas as pd
import time

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
                            format_func=lambda user: f"👤 {user}",
                            key="login_selectbox")
    if st.button("Login"):
        if authenticate(username):
            # Store the authenticated user in session state
            st.session_state.user = username
            st.session_state.df_modified = False  # Flag to track if dataframe is modified
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username")

# Logout button
def logout():
    if st.button("Logout"):
        # Clear the session state variables
        st.session_state.user = None
        st.session_state.df_modified = False
        st.session_state.df = None
        st.success("Logged out")

# Function to render sentences and select boxes
def render_sentences():
    # Retrieve the dataframe from session state or create a new one
    if 'df' not in st.session_state or st.session_state.df is None:
        st.session_state.df = pd.DataFrame(
            {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})

    # Iterate over the dataframe and allow users to tag sentences
    for index, row in st.session_state.df.iterrows():
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"],
                           key=f"tag_selectbox_{index}")
        # Update the dataframe with the selected tag
        st.session_state.df.at[index, "tag"] = tag
        st.session_state.df_modified = True  # Set the modified flag

    # Save changes to the dataframe if it has been modified
    if st.session_state.df_modified:
        st.session_state.df_modified = False  # Reset the modified flag
        save_data()

# Function to save the dataframe
def save_data():
    st.session_state.df.to_csv("tagged_sentences.csv", index=False)
    st.success("Changes saved!")

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
            render_sentences()
        elif user == "Gabi":
            st.title("Gabi's Page")
            st.write("Welcome to Gabi's section!")
            render_sentences()
        elif user == "Ittamar":
            st.title("Ittamar's Page")
            st.write("Welcome to Ittamar's section!")
            render_sentences()
        elif user == "Nurit":
            st.title("Nurit's Page")
            st.write("Welcome to Nurit's section!")
            render_sentences()

        # Add a logout button
        logout()

# Run the app
if __name__ == '__main__':
    main()
