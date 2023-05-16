import streamlit as st
import pandas as pd

def main():
    # Create sidebar with two sections
    st.sidebar.title("Annotation App")
    st.sidebar.header("Data File")
    data_file = st.sidebar.file_uploader("Upload data file", type=["csv"])

    st.sidebar.header("Annotation Page")
    annotation_button = st.sidebar.button("Open Annotation Page")

    if data_file is not None:
        # Read the data file
        data = pd.read_csv(data_file)

        if annotation_button:
            # Display annotation page
            annotated_data = show_annotation_page(data)
            show_annotated_data(annotated_data)


def show_annotation_page(data):
    # Create an empty DataFrame to store annotations
    annotated_data = pd.DataFrame(columns=["Sentence", "Annotation"])

    # Display annotation page for each row in the data file
    for index, row in data.iterrows():
        sentence = row["Sentence"]
        st.write(f"**Sentence:** {sentence}")

        # Create a choice selection for each row
        selected_option = st.selectbox("Choose an option", options=["a", "b", "c", "d"])

        # Perform annotation task here (e.g., save selected_option to a database)
        annotated_data = annotated_data.append({"Sentence": sentence, "Annotation": selected_option}, ignore_index=True)

        st.write("---")  # Add a separator between rows

    return annotated_data


def show_annotated_data(data):
    # Display annotated data file
    st.title("Annotated Data File")
    st.write(data)


if __name__ == "__main__":
    main()
