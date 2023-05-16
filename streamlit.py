import streamlit as st
import pandas as pd

def main():
    # Create sidebar with two sections
    st.sidebar.title("Annotation App")
    st.sidebar.header("Annotation Page")
    annotation_button = st.sidebar.button("Open Annotation Page")

    if annotation_button:
        # Display annotation page
        show_annotation_page()


def show_annotation_page():
    # Sample data and annotations
    data = pd.DataFrame({
        "Sentence": ["This is sentence 1", "This is sentence 2", "This is sentence 3"],
    })
    annotations = pd.DataFrame({
        "Sentence": ["This is sentence 1", "This is sentence 2", "This is sentence 3"],
        "Annotation": ["a", "b", "c"],
    })

    # Display annotation page for each row in the data file
    for index, row in data.iterrows():
        sentence = row["Sentence"]
        st.write(f"**Sentence:** {sentence}")

        # Get the annotation for the current sentence, if available
        annotation_row = annotations.loc[annotations["Sentence"] == sentence]
        selected_option = annotation_row["Annotation"].values[0] if not annotation_row.empty else None

        # Create a choice selection for each row
        selected_option = st.selectbox("Choose an option", options=["a", "b", "c", "d"], index=selected_option)

        # Perform annotation task here (e.g., save selected_option to a database)

        st.write("---")  # Add a separator between rows


if __name__ == "__main__":
    main()
