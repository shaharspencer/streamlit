import streamlit as st
import pandas as pd
import base64

# Load data from CSV file
data = pd.read_csv("your_dataframe.csv")


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
        annotations = pd.DataFrame(columns=["Sentence", "Annotation"])

    if "Annotation" not in annotations.columns:
        annotations["Annotation"] = "a"  # Set default annotation to "a"

    merged = pd.merge(data, annotations[["Sentence", "Annotation"]],
                      on="Sentence", how="outer")
    merged["Annotation"].fillna("a", inplace=True)  # Set default annotation to "a"
    merged.drop_duplicates(inplace=True)  # Remove duplicate columns
    return merged


# Define a function to download the dataframe as a CSV file
def download_dataframe(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_annotations.csv">Download CSV</a>'
    return href


# Main app
def main():
    # Sidebar menu
    st.sidebar.markdown("**Annotations**")

    # Check if the "View Annotations" option is selected
    view_all_annotations = st.sidebar.button("View All Annotations")

    # User Annotations page
    st.sidebar.markdown("---")
    st.sidebar.markdown("**User Annotations**")
    user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])

    if not view_all_annotations:
        # Load user's annotations
        user_annotations = load_annotations(user)

        # Display user's annotations
        st.header(f"{user}'s Annotations")
        for index, row in user_annotations.iterrows():
            st.write(row["Sentence"])
            annotation = st.selectbox("Annotation", options=["a", "b", "c"],
                                      key=f"{user}_tag_selectbox_{index}",
                                      index=ord(row["Annotation"]) - ord("a"))
            user_annotations.at[index, "Annotation"] = annotation
            # Save user's annotations for each selection
            save_annotations(user, user_annotations)

        st.write("Changes saved automatically")

        # Add download button for the user's dataframe
        st.markdown(download_dataframe(user_annotations), unsafe_allow_html=True)

    # View All Annotations page
    st.header("View All Annotations")
    for u in ["Gabi", "Shahar", "Nurit", "Ittamar"]:
        annotations = load_annotations(u)
        st.subheader(f"{u}'s Annotations")
        st.dataframe(annotations)


if __name__ == "__main__":
    main()
