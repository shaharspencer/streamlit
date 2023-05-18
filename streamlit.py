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
        annotations = pd.DataFrame(columns=["Sentence", "Annotation", "Notes"])

    if "Annotation" not in annotations.columns:
        annotations["Annotation"] = "a"  # Set default annotation to "a"

    if "Notes" not in annotations.columns:
        annotations["Notes"] = ""  # Add empty "Notes" column if not present

    merged = pd.merge(data, annotations[["Sentence", "Annotation", "Notes"]],
                      on="Sentence", how="outer")
    merged["Annotation"].fillna("a", inplace=True)  # Set default annotation to "a"
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
    # Sidebar menu
    page = st.sidebar.selectbox("Go to", ["Annotations", "View All Annotations", "Annotation Options Guide"])

    if page == "Annotations":
        st.sidebar.markdown("**Annotations**")
        # Display the Annotations page
        user_annotations_page()

    elif page == "View All Annotations":
        st.sidebar.markdown("**View All Annotations**")
        # Display the View All Annotations page
        view_all_annotations_page()

    elif page == "Annotation Options Guide":
        st.sidebar.markdown("**Annotation Options Guide**")
        # Display the Annotation Options Guide page
        annotation_options_guide()

def user_annotations_page():
    # User Annotations page
    user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])

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

        notes = st.text_area("Notes", value=row["Notes"], key=f"{user}_notes_{index}")
        user_annotations.at[index, "Notes"] = notes

        # Save user's annotations for each selection
        save_annotations(user, user_annotations)

    st.write("Changes saved automatically")

    # Add download button for the user's dataframe
    st.markdown(download_dataframe(user_annotations), unsafe_allow_html=True)

def view_all_annotations_page():
    # View All Annotations page
    st.header("View All Annotations")
    all_annotations = pd.DataFrame()
    for u in ["Gabi", "Shahar", "Nurit", "Ittamar"]:
        annotations = load_annotations(u)
        annotations["Annotator"] = u  # Add "Annotator" column with the annotator's name
        all_annotations = pd.concat([all_annotations, annotations], ignore_index=True)

    st.subheader("All Annotations")
    st.dataframe(all_annotations)

if __name__ == "__main__":
    main()
