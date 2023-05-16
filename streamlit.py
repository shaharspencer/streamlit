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
            st.title("Annotation Page")
            show_annotation_page(data)


def show_annotation_page(data):
    # Display annotation page for each row in the data file
    for index, row in data.iterrows():
        sentence = row["Sentence"]
        st.write(f"**Sentence:** {sentence}")

        # Create a choice selection for each row
        selected_option = st.selectbox("Choose an option", options=["a", "b", "c", "d"])

        # Perform annotation task here (e.g., save selected_option to a database)

        st.write("---")  # Add a separator between rows


if __name__ == "__main__":
    main()
