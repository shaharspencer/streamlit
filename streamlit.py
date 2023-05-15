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

# Main app - User1 section
def user1_page():
    st.title("User1 Page")
    st.write("Welcome to User1's section!")
    # Add user-specific content for User1

# Main app - User2 section
def user2_page():
    st.title("User2 Page")
    st.write("Welcome to User2's section!")
    # Add user-specific content for User2

# Main app - User3 section
def user3_page():
    st.title("User3 Page")
    st.write("Welcome to User3's section!")
    # Add user-specific content for User3

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
