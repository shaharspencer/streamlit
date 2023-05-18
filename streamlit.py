import streamlit as st
import pandas as pd
import base64
import spacy
from spacy import displacy


# Load data from CSV file
data = pd.read_csv("your_dataframe.csv")

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
        annotations = pd.DataFrame(columns=["Sentence", "Tag according to dimension", "Notes on relevant dimension", "Notes"])

    if "Tag according to dimension" not in annotations.columns:
        annotations["Tag according to dimension"] = ""  # Set default annotation to ""

    if "Notes on relevant dimension" not in annotations.columns:
        annotations["Notes on relevant dimension"] = ""  # Add empty "Notes on relevant dimension" column if not present

    if "Notes" not in annotations.columns:
        annotations["Notes"] = ""  # Add empty "Notes" column if not present

    merged = pd.merge(data, annotations[["Sentence", "Tag according to dimension", "Notes on relevant dimension", "Notes"]],
                      on="Sentence", how="outer")
    merged["Tag according to dimension"].fillna("", inplace=True)  # Set default annotation to ""
    merged["Notes on relevant dimension"].fillna("", inplace=True)  # Set default notes to empty string
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
    st.header("Annotation Options Guide")
    # Add content for the Annotation Options Guide page

# Main app
def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #B3C1D9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar menu
    st.sidebar.markdown("**Annotations**")

    # Check if the "View Annotations" option is selected
    view_all_annotations = st.sidebar.button("View All Annotations")

    # User Annotations page
    st.sidebar.markdown("---")
    st.sidebar.markdown("**User Annotations**")
    user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])

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
                    sentence = sentence.replace(token.text, f"<b>{token.text}</b>")

            # Display the modified sentence
            st.markdown(sentence, unsafe_allow_html=True)

            # ... Rest of the code ...

        # ... Rest of the code ...


if __name__ == "__main__":
    main()
