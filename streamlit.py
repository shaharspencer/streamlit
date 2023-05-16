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
        show_annotation_page(selected_user)


def show_annotation_page(user):
    # Read the data file
    data_file = "your_dataframe.csv"
    data = pd.read_csv(data_file)

    # Get or create the annotation data for the selected user
    annotation_file = f"{user}_annotation.csv"
    if "annotation_data" not in st.session_state:
        st.session_state.annotation_data = {}

    if annotation_file not in st.session_state.annotation_data:
        annotation_data = pd.DataFrame(columns=["Sentence", "Annotation"])
        st.session_state.annotation_data[annotation_file] = annotation_data
    else:
        annotation_data = st.session_state.annotation_data[annotation_file]

    # Display annotation page for each row in the data file
    for index, row in data.iterrows():


        for index, row in st.session_state.df.iterrows():
            sentence = row["sentence"]
            st.write(f"**Sentence {index + 1}:** {sentence}")
            tag = st.selectbox("Select a tag", ["a", "b", "c", "d", "e"],
                               key=f"tag_selectbox_{index}")
            # Update the dataframe with the selected tag
            st.session_state.df.at[index, "tag"] = tag

        # # Update the session state with the updated annotation data
        # st.session_state.annotation_data[annotation_file] = annotation_data
        #
        # st.write("---")  # Add a separator between rows


if __name__ == "__main__":
    main()
