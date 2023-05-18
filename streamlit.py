import streamlit as st
import pandas as pd

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
    merged = pd.merge(data, annotations[["Sentence", "Annotation"]],
                      on="Sentence", how="outer")
    merged["Annotation"].fillna("a", inplace=True)  # Set default annotation to "a"
    merged.drop_duplicates(inplace=True)  # Remove duplicate columns
    return merged


# Main app
def main():
    # Sidebar menu
    st.sidebar.markdown("**Annotations**")

    # Check if the "View Annotations" option is selected
    if st.sidebar.button("View All Annotations"):
        st.header("View All Annotations")
        for user in ["Gabi", "Shahar", "Nurit", "Ittamar"]:
            annotations = load_annotations(user)
            st.subheader(f"{user}'s Annotations")
            if not annotations.empty:
                st.dataframe(annotations)
            else:
                st.write("No annotations found for this user.")


if __name__ == "__main__":
    main()
