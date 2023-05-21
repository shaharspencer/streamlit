import os
import pathlib
import tempfile
import urllib


import streamlit as st
import pandas as pd
import base64
import spacy
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""


# Load data from CSV file
data = pd.read_csv("your_dataframe.csv", encoding="ISO-8859-1")
model = "en_core_web_lg"
# Load spaCy model
nlp = spacy.load("en_core_web_lg")


# Define a function to save annotations
def save_annotations(user, annotations):
    file_name = f"{user}_annotations.csv"
    annotations.to_csv(file_name, index=False)


# Define a function to load annotations
def load_annotations(user):
    file_name = f"{user}_annotations.csv"
    try:
        annotations = pd.read_csv(file_name)
    except FileNotFoundError:
        annotations = pd.DataFrame(columns=["Sentence", "Tag according to dimension", "Creativity Score (1-5)", "Notes"])

    if "Tag according to dimension" not in annotations.columns:
        annotations["Tag according to dimension"] = ""  # Set default annotation to ""

    if "Creativity Score (1-5)" not in annotations.columns:
        annotations["Creativity Score (1-5)"] = ""  # Add empty "Notes on relevant dimension" column if not present

    if "Notes" not in annotations.columns:
        annotations["Notes"] = ""  # Add empty "Notes" column if not present

    merged = pd.merge(data, annotations[["Sentence", "Tag according to dimension", "Creativity Score (1-5)", "Notes"]],
                      on="Sentence", how="outer")
    merged["Tag according to dimension"].fillna("", inplace=True)  # Set default annotation to ""
    merged["Creativity Score (1-5)"].fillna("", inplace=True)  # Set default notes to empty string
    merged["Notes"].fillna("", inplace=True)  # Set default notes to empty string
    merged.drop_duplicates(inplace=True)  # Remove duplicate columns
    return merged


# Define a function to download the dataframe as a CSV file
def download_dataframe(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_annotations.csv">Download CSV</a>'
    return href


# Annotation Options Guide page
def annotation_options_guide():
    st.header("Annotation information")
    for index, row in data.iterrows():
        sentence = row["Sentence"]
        doc = nlp(sentence)
        # Render the token in bold
        for token in doc:
            if token.i == row["index of verb"]:
                new_sentence = sentence.replace(token.text,
                                                f"<b>{token.text}</b>")
        sentence_number = index + 1
        st.markdown(f"Sentence {sentence_number}: {new_sentence}",
                    unsafe_allow_html=True)

        sent = nlp(sentence)
        html = displacy.render(sent, style="dep")

        st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)




# Main app
def main():
    # Sidebar menu
    st.sidebar.markdown("**Annotations**")

    # Check if the "View Annotations" option is selected
    view_all_annotations = st.sidebar.button("View All Annotations")

    # User Annotations page
    st.sidebar.markdown("---")
    st.sidebar.markdown("**User Annotations**")
    user = st.sidebar.selectbox("Select User",
                                ["Nurit", "Ittamar", "Gabi", "Shahar"])

    # Annotation Options Guide page
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Annotation Options Guide**")
    if st.sidebar.button("Go to Annotation Options Guide"):
        # Render the Annotation Options Guide page
        annotation_options_guide()

    if not view_all_annotations:
        # Load user's annotations
        user_annotations = load_annotations(user)

        # Display user's annotations
        st.header(f"{user}'s Annotations")
        for index, row in user_annotations.iterrows():


            sentence = row["Sentence"]
            doc = nlp(sentence)
            # Render the token in bold
            for token in doc:
                if token.i == row["index of verb"]:

                    new_sentence = sentence.replace(token.text,
                                                           f"<b>{token.text}</b>")
            sentence_number = index + 1
            st.markdown(f"Sentence {sentence_number}: {new_sentence}",
                        unsafe_allow_html=True)


            # Display expand button under the sentence
            expand_button = st.button("Expand",
                                      key=f"{user}_expand_button_{index}")
            if expand_button:
                # Toggle visibility of extra data
                if f"{user}_expanded_{index}" not in st.session_state:
                    st.session_state[f"{user}_expanded_{index}"] = {
                        "extra_data": True,

                    }
                else:
                    st.session_state[f"{user}_expanded_{index}"]["extra_data"] = not \
                        st.session_state[f"{user}_expanded_{index}"]["extra_data"]

            # Display extra data if expanded for the current user
            if f"{user}_expanded_{index}" in st.session_state and \
                    st.session_state[f"{user}_expanded_{index}"]["extra_data"]:
                # Iterate over all columns except "Sentence", "Tag according to dimension", "Notes on relevant dimension", and "Notes"
                for column in data.columns:
                    if column not in ["Sentence", "Tag according to dimension",
                                      "Creativity Score (1-5)", "Notes"]:
                        st.write(f"{column}: {row[column]}")


            tag_options = ["",
                "ordinary",
                "creative",
                "spelling variant",
                "wrong lemma",
                "not a verb",
                "algorithm error",
                "not English"
            ]
            annotation = st.selectbox("Tag according to dimension", options= tag_options, key=f"{user}_tag_selectbox_{index}", index=tag_options.index(row["Tag according to dimension"]))
            user_annotations.at[
                index, "Tag according to dimension"] = annotation

            notes_relevant_dimension = st.text_area("Creativity Score (1-5)",
                                                    value=row["Creativity Score (1-5)"],
                                                    key=f"{user}_notes_relevant_dimension_{index}")
            user_annotations.at[index, "Creativity Score (1-5)"] = notes_relevant_dimension

            notes = st.text_area("Notes",
                                 value=row["Notes"],
                                 key=f"{user}_notes_{index}")
            user_annotations.at[index, "Notes"] = notes

            # Save user's annotations for each selection
            save_annotations(user, user_annotations)

        st.write("Changes saved automatically")

        # Add download button for the user's dataframe
        st.markdown(download_dataframe(user_annotations),
                    unsafe_allow_html=True)

    # View All Annotations section
    if view_all_annotations:
        st.header("View All Annotations")
        all_annotations = pd.DataFrame()
        for u in ["Nurit", "Ittamar", "Gabi", "Shahar"]:
            annotations = load_annotations(u)
            annotations["Annotator"] = u  # Add "Annotator" column with the annotator's name
            all_annotations = pd.concat([all_annotations, annotations], ignore_index=True)

        st.subheader("All Annotations")
        st.dataframe(all_annotations)

        # Download all annotations as a single CSV file
        st.markdown(download_dataframe(all_annotations), unsafe_allow_html=True)


if __name__ == "__main__":
    main()