import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Replace with your FastAPI server address


def login_user(username, password):
    data = {"username": username, "password": password}
    return requests.post(f"{BASE_URL}/auth/login/", params=data)


def login_main():
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            response = login_user(username, password)
            if response.status_code == 200:
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Please try again.")


if __name__ == "__main__":

    login_main()
