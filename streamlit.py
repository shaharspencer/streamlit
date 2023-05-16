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
    if 'df' not in st.session_state or st.session_state.df is None:
        st.session_state.df = pd.DataFrame(
            {"sentence": ["Sentence 1", "Sentence 2", "Sentence 3"]})

    # Get or create the annotation data for the selected user
    annotation_file = f"{user}_annotation.csv"
    if annotation_file not in st.session_state:
        if not st.session_state.df.empty:
            annotation_data = pd.DataFrame(columns=["Sentence", "Annotation"])
            annotation_data["Sentence"] = st.session_state.df["sentence"]
            annotation_data.to_csv(annotation_file, index=False)
        else:
            annotation_data = pd.DataFrame()
        st.session_state[annotation_file] = annotation_data
    else:
        annotation_data = st.session_state[annotation_file]

    # Iterate over the dataframe and allow users to tag sentences
    for index, row in st.session_state.df.iterrows():
        sentence = row["sentence"]
        st.write(f"**Sentence {index + 1}:** {sentence}")
        selected_option = get_selected_option(annotation_data, sentence)
        tag = st.selectbox("Select a tag", ["", "a", "b", "c", "d", "e"],
                           index=selected_option,
                           key=f"tag_selectbox_{user}_{index}")
        # Update the annotation data for the current user
        update_annotation_data(annotation_data, sentence, tag)
        annotation_data.to_csv(annotation_file, index=False)

def get_selected_option(annotation_data, sentence):
    annotation_row = annotation_data.loc[annotation_data["Sentence"] == sentence]
    if not annotation_row.empty:
        return annotation_row["Annotation"].values[0]
    return 0

def update_annotation_data(annotation_data, sentence, tag):
    annotation_row = annotation_data.loc[annotation_data["Sentence"] == sentence]
    if not annotation_row.empty:
        annotation_data.loc[annotation_row.index, "Annotation"] = tag
    else:
        annotation_data = annotation_data.append({"Sentence": sentence, "Annotation": tag}, ignore_index=True)

if __name__ == "__main__":
    main()
