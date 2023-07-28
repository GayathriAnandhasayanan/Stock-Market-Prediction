import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Replace with your FastAPI server address


# Function to mark a stock as favorite
def mark_favorite(stock_id):
    response = requests.post(f"{BASE_URL}/favorite/{stock_id}/")
    if response.status_code == 200:
        st.success("Stock marked as favorite!")
    elif response.status_code == 404:
        st.error("Stock not found.")
    else:
        st.error("Failed to mark stock as favorite. Please try again later.")


# Main function for the "My Stocks" page
def my_stocks_main():
    st.title("My Stocks")

    # Fetch the user's favorite stocks from the backend
    response = requests.get(f"{BASE_URL}/favorite/")
    if response.status_code == 200:
        favorite_stocks = response.json()
        for stock in favorite_stocks:
            st.write(f"{stock['name']} ({stock['symbol']})")
            if st.button("Mark as Favorite"):
                mark_favorite(stock['id'])
            st.write("---")
    else:
        st.error("Failed to fetch favorite stocks. Please try again later.")


# Main function for the Stocks page
def stocks_main():
    st.title("Stocks")

    # Fetch all stocks from the backend
    response = requests.get(f"{BASE_URL}/stocks/")
    if response.status_code == 200:
        all_stocks = response.json()
        for stock in all_stocks:
            st.write(f"{stock['name']} ({stock['symbol']})")
            if st.button("Mark as Favorite"):
                mark_favorite(stock['id'])
            st.write("---")
    else:
        st.error("Failed to fetch stocks. Please try again later.")


stocks_main()
