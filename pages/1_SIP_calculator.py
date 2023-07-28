import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def get_stock_data(stock_code, start_date, end_date):
    stock_data = yf.download(stock_code, start=start_date, end=end_date)
    return stock_data


def calculate_sip_investment(principal, monthly_investment, stock_data):
    # Calculate the SIP investment value over time
    investments = [principal]
    investment_dates = stock_data[::30].index  # Monthly investment on the 30th day of each month
    for i, date in enumerate(investment_dates[:-1]):
        current_value = investments[-1]
        monthly_investment_value = current_value + monthly_investment
        shares_purchased = monthly_investment_value / stock_data.loc[date]['Close']
        investments.append(shares_purchased * stock_data.loc[investment_dates[i + 1]]['Close'])
    return investments[:-1], investment_dates[:-1]


def calculate_roi(stock_data):
    # Calculate ROI for the investment time interval
    starting_value = stock_data.iloc[0]['Close']
    ending_value = stock_data.iloc[-1]['Close']
    roi = (ending_value - starting_value) / starting_value * 100

    return roi


def calculate_roi_yoy(stock_data):
    # Calculate ROI Year-on-Year (YoY) for the investment time interval
    closing_prices = stock_data['Close']
    roi_yoy = (closing_prices / closing_prices.shift(12) - 1) * 100

    return roi_yoy


def main():
    st.title("SIP Calculator for Stocks")

    # Set up the sidebar layout
    st.sidebar.title("User Inputs")

    # Input widgets for stock codes
    stock_code = st.sidebar.text_input("Enter Stock Code", 'GOOGL')

    # Input widgets for SIP calculation
    start_date = st.sidebar.date_input("Select start date", pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input("Select end date", pd.to_datetime('today'))
    initial_investment = st.sidebar.number_input("Enter the initial investment amount ($)", min_value=0, value=1000)
    monthly_investment = st.sidebar.number_input("Enter the monthly investment amount ($)", min_value=0, value=100)

    # Calculate the number of months
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    # Get historical stock data for the selected stock
    stock_data = get_stock_data(stock_code, start_date, end_date)

    if len(stock_data) == 0:
        st.sidebar.warning("Invalid stock code or no historical data available.")
        return

    # Calculate SIP investment for the selected stock
    sip_investment, investment_dates = calculate_sip_investment(initial_investment, monthly_investment, stock_data)

    # Create a DataFrame to store SIP investment data
    data = {
        'Date': investment_dates,
        'SIP Investment Value': sip_investment
    }
    df = pd.DataFrame(data)

    # Calculate total investment amount
    total_investment = initial_investment + (monthly_investment * num_months)

    # Calculate ROI and ROI YoY for the investment
    roi = calculate_roi(stock_data)
    roi_yoy = calculate_roi_yoy(stock_data)

    # Calculate the current value of investment
    current_investment_value = df['SIP Investment Value'].iloc[-1]

    # Display SIP investment values over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['SIP Investment Value'])
    plt.xlabel('Date')
    plt.ylabel('Investment Value ($)')
    plt.title('SIP Investment Value Over Time')
    plt.grid(True)

    st.pyplot(plt)

    # Display the calculated metrics
    st.header("Investment Metrics")
    st.write(f"Total Investment Amount: ${total_investment:.2f}")
    st.write(f"Number of Months: {num_months}")
    st.write(f"ROI: {roi:.2f}%")
    st.write(f"ROI Year-on-Year (YoY):")
    st.dataframe(roi_yoy.rename("ROI YoY (%)"))
    st.write(f"Current Investment Value: ${current_investment_value:.2f}")


if __name__ == "__main__":
    main()
