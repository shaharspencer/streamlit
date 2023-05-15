import streamlit as st
import pandas as pd

# Define the list of valid users
valid_users = ["user1", "user2", "user3"]

# User authentication
def authenticate(username):
    # Check if the provided username is in the list of valid users
    if username in valid_users:
        return True
    else:
        return False

# Login form
def login():
    username = st.selectbox("Select User", valid_users, format_func=lambda user: f"👤 {user}")
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
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"])
        # Perform any necessary processing or storage of the tag

# Main app - User1 section
def user1_page():
    st.title("User1 Page")
    st.write("Welcome to User1's section!")
    # Load or generate a dataframe for User1
    dataframe_user1 = pd.DataFrame({"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})
    # Call the tagging function for User1
    tag_sentences(dataframe_user1)

# Main app - User2 section
def user2_page():
    st.title("User2 Page")
    st.write("Welcome to User2's section!")
    # Load or generate a dataframe for User2
    dataframe_user2 = pd.DataFrame({"sentence": ["Sentence A", "Sentence B", "Sentence C"]})
    # Call the tagging function for User2
    tag_sentences(dataframe_user2)

# Main app - User3 section
def user3_page():
    st.title("User3 Page")
    st.write("Welcome to User3's section!")
    # Load or generate a dataframe for User3
    dataframe_user3 = pd.DataFrame({"sentence": ["Example 1", "Example 2", "Example 3"]})
    # Call the tagging function for User3
    tag_sentences(dataframe_user3)

# Main app
def main():
    st.title("Multiple User Streamlit App")

    if 'user' not in st.session_state or st.session_state.user is None:
        login()
    else:
        user = st.session_state.user

        # Show different pages based on the selected user
        if user == "user1":
            user1_page()
        elif user == "user2":
            user2_page()
        elif user == "user3":
            user3_page()

        # Add a logout button in the sidebar
        st.sidebar.button("Logout", on_click=logout)

# Run the app
if __name__ == '__main__':
    main()
