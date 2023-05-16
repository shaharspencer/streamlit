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
    # Sample data
    data = pd.DataFrame({
        "Sentence": ["This is sentence 1", "This is sentence 2", "This is sentence 3"],
    })

    # Get or create the annotation data for the selected user
    annotation_file = f"{user}_annotation.csv"
    if "annotation_data" not in st.session_state:
        st.session_state.annotation_data = {}
    if annotation_file not in st.session_state.annotation_data:
        st.session_state.annotation_data[annotation_file] = pd.DataFrame(columns=["Sentence", "Annotation"])

    annotation_data = st.session_state.annotation_data[annotation_file]

    # Display annotation page for each row in the data file
    for index, row in data.iterrows():
        sentence = row["Sentence"]
        st.write(f"**Sentence:** {sentence}")

        # Get the annotation for the current sentence, if available
        annotation_row = annotation_data.loc[annotation_data["Sentence"] == sentence]
        selected_option = annotation_row["Annotation"].values[0] if not annotation_row.empty else None

        # Create a choice selection for each row
        selected_option = st.selectbox("Choose an option", options=["a", "b", "c", "d"], index=selected_option)

        # Update the annotation in the session state
        if not annotation_row.empty:
            annotation_data.loc[annotation_row.index, "Annotation"] = selected_option
        else:
            annotation_data = annotation_data.append({"Sentence": sentence, "Annotation": selected_option},
                                                     ignore_index=True)

        # Update the session state with the updated annotation data
        st.session_state.annotation_data[annotation_file] = annotation_data

        st.write("---")  # Add a separator between rows


if __name__ == "__main__":
    main()
