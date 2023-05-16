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

    # Retrieve the user's dataframe from session state or create a new one
    user_df_key = f"{user}_df"
    if user_df_key not in st.session_state or st.session_state[user_df_key] is None:
        st.session_state[user_df_key] = pd.DataFrame(
            {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"], "tag": [""] * 3})

    # Get the user's dataframe
    user_df = st.session_state[user_df_key]

    # Iterate over the dataframe and allow the user to tag sentences
    for index, row in user_df.iterrows():
        options = ["", "a", "b", "c", "d", "e"]
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        default_index = options.index(row["tag"])
        tag = st.selectbox(label =f"Select a tag for Sentence {index + 1}", options=["", "a", "b", "c", "d", "e"],
                           key=f"{user}_tag_selectbox_{index}", index=default_index)
        # Update the dataframe with the selected tag
        user_df.at[index, "tag"] = tag

    # Add a save button to save changes to the user's dataframe
    if st.button("Save Changes"):
        # Save the user's dataframe to a file
        user_annotation_file = f"{user}_annotation.csv"
        user_df.to_csv(user_annotation_file, index=False)
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
