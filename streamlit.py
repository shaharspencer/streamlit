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
    merged = pd.merge(data, annotations, on="Sentence", how="outer")
    merged["Annotation"].fillna("a", inplace=True)  # Set default annotation to "a"
    return merged

# Main app
def main():
    # Get user name
    user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])

    # Load user's annotations
    user_annotations = load_annotations(user)

    # Display user's annotations
    for index, row in user_annotations.iterrows():
        st.write(row["Sentence"])
        annotation = st.selectbox("Annotation", choices=["a", "b", "c"], key=f"{user}_tag_selectbox_{index}", index=ord(row["Annotation"]) - ord("a"))
        user_annotations.at[index, "Annotation"] = annotation

        # Save user's annotations when changes are made
        save_annotations(user, user_annotations)

    st.write("Changes saved automatically")

if __name__ == "__main__":
    main()
