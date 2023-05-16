import streamlit as st
import pandas as pd

def main():
    # Create sidebar with two sections
    st.sidebar.title("Annotation App")
    st.sidebar.header("Annotation Pages")
    user_list = ["User 1", "User 2", "User 3"]  # List of users
    selected_user = st.sidebar.selectbox("Select user", user_list)

    annotation_button = st.sidebar.button("Open Annotation Page")

    if annotation_button:
        # Display annotation page
        with st.spinner():
            show_annotation_page(selected_user)


def show_annotation_page(user):
    # Read the data file
    if 'df' not in st.session_state or st.session_state.df is None:
        st.session_state.df = pd.DataFrame(
            {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})

    # Iterate over the dataframe and allow users to tag sentences
    for index, row in st.session_state.df.iterrows():
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"],
                           key=f"tag_selectbox_{index}",
                           index=get_current_tag_index(user, index))
        # Update the dataframe with the selected tag
        st.session_state.df.at[index, get_user_column(user)] = tag

    # Display annotation page for each row in the data file


def get_current_tag_index(user, index):
    column = get_user_column(user)
    if column in st.session_state.df.columns:
        tag = st.session_state.df.at[index, column]
        if tag in ["a", "b", "c", "d", "e"]:
            return ["a", "b", "c", "d", "e"].index(tag)
    return 0


def get_user_column(user):
    return f"{user}_tag"


if __name__ == "__main__":
    main()
