# Stock Market Analysis and Price Prediction Web App

## Overview
This web application provides users with stock market technical analysis and future price prediction using deep learning algorithms. Users can sign up and sign in to access personalized features and manage their shortlisted stocks. The app also allows users to set notifications for specific stock values and provides detailed technical analysis for selected stocks.

## Features

1. **Sign Up and Sign In**: Users can create an account and log in to access personalized features.

2. **Personalized Stock List**: Upon login, users can view details about their shortlisted stocks, including their current values. The stock list is automatically updated with each page refresh.

3. **Manage Shortlisted Stocks**: Users can easily add or remove stocks from their shortlist.

4. **Volume and Value Intention**: Users have the option to specify the volumes and values they intend to purchase or sell.

5. **Stock Notifications**: Users can set up notifications for specific stock values in the future.

6. **Stock Details and Technical Analysis**: When a user selects a particular stock, the app displays detailed information about the stock, including technical analysis.

7. **Future Price Prediction**: The app provides price predictions for selected stocks using deep learning algorithms.

8. **Stock Comparison**: Users can compare the technical analysis of multiple stocks (up to 3) for better insights.

## Technologies Used

- Frontend: Streamlit (Python)
- Backend: FastAPI (Python)
- Database: PostgreSQL with psycopg2 (Python)

## Installation

To run the application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/stock-market-app.git
   cd stock-market-app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI backend:
   ```bash
   uvicorn main:app --reload
   ```
   The FastAPI server will be accessible at `http://127.0.0.1:8000`.

5. Open a new terminal window (keeping the backend running) and run the Streamlit frontend:
   ```bash
   streamlit run main.py
   ```
   The Streamlit app will be accessible at `http://localhost:8501`.

## Usage

1. Sign Up and Sign In:
   - Access the web app in your browser at `http://localhost:8501`.
   - Sign up with your username and password.
   - Sign in with your registered credentials.

2. Shortlisted Stocks:
   - Upon signing in, you will see details about your shortlisted stocks and their current values.
   - The list of stocks will be updated each time you refresh the page.
   - You can add or remove any stock from the list.

4. Stock Notification:
   - You can set notifications for specific stock values in the future.

5. Stock Details and Prediction:
   - Click on a particular stock to view its details and technical analysis.
   - The price prediction for the stock will also be displayed.
   - You can compare similar stocks based on technical analysis.

## Contribution
- Amey Gawade
- Amir Mobayen
- Gayathri Anandhasayanan