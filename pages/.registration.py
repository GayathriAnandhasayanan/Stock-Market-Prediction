# pages/.registration.py

import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Replace with your FastAPI server address


def register_user(username, password):
    data = {"username": username, "password": password}
    return requests.post(f"{BASE_URL}/auth/register/", params=data)


def registration_main():
    st.title("User Registration")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            response = register_user(username, password)
            if response.status_code == 200:
                st.success(f"Username {username} Successfully Registered")
            elif response.status_code == 400:
                st.error("Username already exists.")
            else:
                st.error("Registration failed. Please try again later.")

registration_main()