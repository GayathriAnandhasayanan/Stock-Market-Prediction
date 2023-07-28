import streamlit as st
def readme_main():
    st.markdown(get_readme_contents(), unsafe_allow_html=True)


def get_readme_contents():
    with open("README.md", "r") as readme_file:
        contents = readme_file.read()
    return contents


readme_main()
