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
def tag_sentences(user):
    st.title(f"{user}'s Annotation Page")
    st.write("Tag sentences with options 'a', 'b', 'c', 'd', 'e'")

    # Read the user's dataframe from a CSV file
    user_dataframe_file = "your_dataframe.csv"
    user_df = pd.read_csv(user_dataframe_file)

    # Iterate over the dataframe and allow the user to tag sentences
    for index, row in user_df.iterrows():
        sentence = row["Sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        tag = st.selectbox(f"Select a tag for Sentence {index + 1}", ["", "a", "b", "c", "d", "e"],
                           key=f"{user}_tag_selectbox_{index}", index=row["Tag"])
        # Update the dataframe with the selected tag
        user_df.at[index, "Tag"] = tag

    # Add a save button to save changes to the user's dataframe
    if st.button("Save Changes"):
        # Save the updated dataframe to the CSV file
        user_df.to_csv(user_dataframe_file, index=False)
        st.success("Changes saved!")

# Main app
def main():
    st.title("Multiple User Streamlit App")

    if 'user' not in st.session_state or st.session_state.user is None:
        login()
    else:
        user = st.session_state.user

        if user in valid_users:
            tag_sentences(user)
        else:
            st.error("Invalid user")

        # Add a logout button
        logout()

if __name__ == "__main__":
    main()
