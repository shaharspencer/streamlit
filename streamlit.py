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
    merged = pd.merge(data, annotations[["Sentence", "Annotation"]], on="Sentence", how="outer")
    merged["Annotation"].fillna("a", inplace=True)
    merged.drop_duplicates(inplace=True)
    return merged

# Define a function to download the merged dataframe as a CSV file
def download_merged_dataframe(merged_dataframe):
    csv = merged_dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_annotations.csv">Download Merged CSV</a>'
    return href

# Main app
def main():
    st.sidebar.markdown("**Annotations**")

    view_all_annotations = st.sidebar.button("View All Annotations")

    if view_all_annotations:
        st.header("View All Annotations")
        merged_annotations = pd.DataFrame(data["Sentence"])
        for user in ["Gabi", "Shahar", "Nurit", "Ittamar"]:
            annotations = load_annotations(user)
            merged_annotations = pd.merge(merged_annotations, annotations[["Sentence", "Annotation"]],
                                          on="Sentence", how="left")
        st.dataframe(merged_annotations)
        st.markdown(download_merged_dataframe(merged_annotations), unsafe_allow_html=True)

        # Show user-specific annotations
        st.sidebar.markdown("**User Annotations**")
        user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])
        user_annotations = load_annotations(user)
        st.header(f"{user}'s Annotations")
        for index, row in user_annotations.iterrows():
            st.write(row["Sentence"])
            annotation = st.selectbox("Annotation", options=["a", "b", "c"], key=f"{user}_tag_selectbox_{index}",
                                      index=ord(row["Annotation"]) - ord("a"))
            user_annotations.at[index, "Annotation"] = annotation
            save_annotations(user, user_annotations)

        st.write("Changes saved automatically")
        st.markdown(download_merged_dataframe(user_annotations), unsafe_allow_html=True)

    else:
        # Show user-specific annotations
        st.sidebar.markdown("---")
        st.sidebar.markdown("**User Annotations**")
        user = st.sidebar.selectbox("Select User", ["Gabi", "Shahar", "Nurit", "Ittamar"])
        user_annotations = load_annotations(user)
        st.header(f"{user}'s Annotations")
        for index, row in user_annotations.iterrows():
            st.write(row["Sentence"])
            annotation = st.selectbox("Annotation", options=["a", "b", "c"], key=f"{user}_tag_selectbox_{index}",
                                      index=ord(row["Annotation"]) - ord("a"))
            user_annotations.at[index, "Annotation"] = annotation
            save_annotations(user, user_annotations)

        st.write("Changes saved automatically")
        st.markdown(download_merged_dataframe(user_annotations), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
