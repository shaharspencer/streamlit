import streamlit as st
import pandas as pd
import base64
import spacy
from spacy import displacy


# Load data from CSV file
data = pd.read_csv(r"21_05_2023/dep_struct_rarest_sents_by_entropy_2023_05_21.csv",
                   encoding="ISO-8859-1")

# Load spaCy model
nlp = spacy.load("en_core_web_lg")


# Define a function to save annotations
def save_annotations(user, annotations):
    file_name = f"{user}_annotations.csv"
    annotations.to_csv(file_name, index=False,
                       columns=["Sentence", "Tag according to dimension",
                                "Creativity Scale",
                                "Notes on relevant dimension", "Notes"])


# Define a function to load annotations
def load_annotations(user):
    file_name = f"{user}_annotations.csv"
    try:
        annotations = pd.read_csv(file_name)
    except FileNotFoundError:
        annotations = pd.DataFrame(columns=["Sentence", "Tag according to dimension", "Creativity Scale",
                                    "Notes on relevant dimension", "Notes",
                                    ])

    if "Tag according to dimension" not in annotations.columns:
        annotations["Tag according to dimension"] = ""  # Set default annotation to ""

    if "Notes on relevant dimension" not in annotations.columns:
        annotations["Notes on relevant dimension"] = ""  # Add empty "Notes on relevant dimension" column if not present

    if "Notes" not in annotations.columns:
        annotations["Notes"] = ""  # Add empty "Notes" column if not present

    if "Creativity Scale" not in annotations.columns:
        annotations["Creativity Scale"] = ""  # Add empty "Scale" column if not present

    merged = pd.merge(data, annotations[["Sentence", "Tag according to dimension", "Creativity Scale",
                                    "Notes on relevant dimension", "Notes",
                                    ]],
                      on="Sentence", how="outer")
    merged["Tag according to dimension"].fillna("", inplace=True)  # Set default annotation to ""
    merged["Notes on relevant dimension"].fillna("", inplace=True)  # Set default notes to empty string
    merged["Notes"].fillna("", inplace=True)  # Set default notes to empty string
    merged.drop_duplicates(inplace=True)  # Remove duplicate columns
    return merged


# Define a function to download the dataframe as a CSV file
def download_dataframe(dataframe):
    csv = dataframe.to_csv(index=False,
                           )

    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_annotations.csv">Download CSV</a>'
    return href


# Annotation Options Guide page
def annotation_options_guide():
    st.header("Annotation Options Guide")
    # Add content for the Annotation Options Guide page


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
            # Iterate over the tokens in the sentence
            for token in doc:
                if token.i == row["index of verb"]:
                    # Render the token in bold
                    new_sentence = sentence.replace(token.text,
                                                f"<b>{token.text}</b>")
            sentence_number = index + 1
            st.markdown(f"Sentence {sentence_number}: {new_sentence}", unsafe_allow_html=True)

            # Display expand button under the sentence
            expand_button = st.button("Expand",
                                      key=f"{user}_expand_button_{index}")
            if expand_button:
                # Toggle visibility of extra data and dependency tree for the current user only
                if f"{user}_expanded_{index}" not in st.session_state:
                    st.session_state[f"{user}_expanded_{index}"] = {
                        "extra_data": True,
                        "dependency_tree": False
                    }
                else:
                    st.session_state[f"{user}_expanded_{index}"]["extra_data"] = not \
                        st.session_state[f"{user}_expanded_{index}"]["extra_data"]

            # Display extra data if expanded for the current user
            if f"{user}_expanded_{index}" in st.session_state and \
                    st.session_state[f"{user}_expanded_{index}"]["extra_data"]:
                # Iterate over all columns except "Sentence", "Tag according to dimension", "Notes on relevant dimension", and "Notes"
                for column in data.columns:
                    if column not in ["Sentence", "Tag according to dimension", "Creativity Scale",
                                    "Notes on relevant dimension", "Notes",
                                    ]:
                        st.write(f"{column}: {row[column]}")

            # Display dependency tree button
            dependency_tree_button = st.button("Show Dependency Tree",
                                               key=f"{user}_dependency_tree_button_{index}")
            if dependency_tree_button:
                # Toggle visibility of the dependency tree for the current user only
                if f"{user}_expanded_{index}" not in st.session_state:
                    st.session_state[f"{user}_expanded_{index}"] = {
                        "extra_data": False,
                        "dependency_tree": True
                    }
                else:
                    st.session_state[f"{user}_expanded_{index}"]["dependency_tree"] = not \
                        st.session_state[f"{user}_expanded_{index}"]["dependency_tree"]

            # Display dependency tree if expanded for the current user
            if f"{user}_expanded_{index}" in st.session_state and \
                    st.session_state[f"{user}_expanded_{index}"]["dependency_tree"]:
                # Display the dependency tree for the current sentence
                sent = nlp(sentence)
                svg = displacy.render(sent, style="dep")
                st.write(svg, unsafe_allow_html=True)

            annotation = st.selectbox("Tag according to dimension", options=[
                "ordinary",
                "creative",
                "spelling variant",
                "wrong lemma",
                "not a verb",
                "algorithm error",
                "not English"
            ], key=f"{user}_tag_selectbox_{index}")
            user_annotations.at[
                index, "Tag according to dimension"] = annotation

            notes_relevant_dimension = st.text_area("Notes on relevant dimension",
                                                    value=row["Notes on relevant dimension"],
                                                    key=f"{user}_notes_relevant_dimension_{index}")
            user_annotations.at[index, "Notes on relevant dimension"] = notes_relevant_dimension

            scale = st.selectbox("Creativity Scale (1-5)",
                                 options=[1, 2, 3, 4, 5],
                                 key= f"{user}_creativity_scale_{index}"
                                )
            user_annotations.at[index, "Creativity Scale"] = scale

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