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
                            format_func=lambda user: f"👤 {user}",
                            key="login_selectbox")
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
        # Clear the session state variables
        st.session_state.user = None
        st.success("Logged out")

# Function to tag sentences
def tag_sentences():
    st.title("Tag Sentences")
    st.write("Tag sentences with options 'a', 'b', 'c', 'd', 'e'")

    # Retrieve the annotation data for the current user or create a new one
    user_annotation_file = f"{st.session_state.user}_annotation.csv"
    if user_annotation_file not in st.session_state:
        st.session_state[user_annotation_file] = pd.DataFrame(
            {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})

    annotation_data = st.session_state[user_annotation_file]

    # Iterate over the annotation data and allow the user to tag sentences
    for index, row in annotation_data.iterrows():
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"],
                           key=f"tag_selectbox_{index}")
        # Update the annotation data with the selected tag
        annotation_data.at[index, "tag"] = tag

    # Add a save button to save changes to the annotation data
    if st.button("Save Changes"):
        annotation_data.to_csv(user_annotation_file, index=False)
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
            tag_sentences()
        elif user == "Gabi":
            st.title("Gabi's Page")
            st.write("Welcome to Gabi's section!")
            tag_sentences()
        elif user == "Ittamar":
            st.title("Ittamar's Page")
            st.write("Welcome to Ittamar's section!")
            tag_sentences()
        elif user == "Nurit":
            st.title("Nurit's Page")
            st.write("Welcome to Nurit's section!")
            tag_sentences()

        # Add a logout button
        logout()

if __name__ == "__main__":
    main()
