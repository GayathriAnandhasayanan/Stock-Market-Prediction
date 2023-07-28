import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import finnhub

def get_stock_data(stock_code, start_date, end_date):
    stock_data = yf.download(stock_code, start=start_date, end=end_date)
    return stock_data


def get_company_name(stock_code):
    try:
        stock_info = yf.Ticker(stock_code)
        company_name = stock_info.info['longName']
        return company_name
    except:
        return "Invalid stock code"


def calculate_daily_changes(combined_data):
    # Calculate daily percentage changes for each stock
    daily_changes = combined_data.copy()
    for column in daily_changes.columns[1:]:
        daily_changes[column] = daily_changes[column].pct_change() * 100

    # Drop the first row since it will have NaN values
    daily_changes.dropna(inplace=True)

    # Set 'Date' as the index again to avoid it being included in the mean calculation
    daily_changes.set_index('Date', inplace=True)

    return daily_changes



def calculate_roi(stock_data):
    # Calculate ROI for the investment time interval
    starting_value = stock_data.iloc[0]['Close']
    ending_value = stock_data.iloc[-1]['Close']
    roi = (ending_value - starting_value) / starting_value * 100

    return roi

def calculate_dividend_yield(stock_code, start_date, end_date):
    stock_data = yf.download(stock_code, start=start_date, end=end_date)

    if 'Dividends' not in stock_data.columns:
        return 0

    dividends = stock_data['Dividends'].sum()
    closing_price_start = stock_data.iloc[0]['Close']
    dividend_yield = (dividends / closing_price_start) * 100

    return dividend_yield



def main():
    st.title("Stock Comparison")

    # Set up the sidebar layout
    st.sidebar.title("User Inputs")

    # Input widgets for stock codes
    stock_code_1 = st.sidebar.text_input("Enter Stock Code 1", 'AAPL')
    stock_name_1 = get_company_name(stock_code_1)

    stock_code_2 = st.sidebar.text_input("Enter Stock Code 2", 'GOOGL')
    stock_name_2 = get_company_name(stock_code_2)

    stock_code_3 = st.sidebar.text_input("Enter Stock Code 3", 'MSFT')
    stock_name_3 = get_company_name(stock_code_3)

    # Radio button to choose between start date and time interval
    date_option = st.sidebar.radio("Select Date Option", ["Specific Dates", "Time Interval"])

    if date_option == "Specific Dates":
        # Input widgets for specific start and end dates
        start_date = st.sidebar.date_input("Select start date", pd.to_datetime('2023-01-01'))
        end_date = st.sidebar.date_input("Select end date", pd.to_datetime('2023-07-01'))
    else:
        # Input widget for time interval
        time_intervals = ["15 days", "30 days", "90 days", "180 days", "52 weeks", "1 year", "2 years", "5 years"]
        selected_interval = st.sidebar.selectbox("Select time interval", time_intervals)

        # Calculate start and end dates based on the selected time interval
        end_date = pd.to_datetime('today')
        if selected_interval == "15 days":
            start_date = end_date - pd.DateOffset(days=15)
        elif selected_interval == "30 days":
            start_date = end_date - pd.DateOffset(days=30)
        elif selected_interval == "90 days":
            start_date = end_date - pd.DateOffset(days=90)
        elif selected_interval == "180 days":
            start_date = end_date - pd.DateOffset(days=180)
        elif selected_interval == "52 weeks":
            start_date = end_date - pd.DateOffset(weeks=52)
        elif selected_interval == "1 year":
            start_date = end_date - pd.DateOffset(years=1)
        elif selected_interval == "2 years":
            start_date = end_date - pd.DateOffset(years=2)
        elif selected_interval == "5 years":
            start_date = end_date - pd.DateOffset(years=5)
        else:
            # Default to 30 days
            start_date = end_date - pd.DateOffset(days=30)

    # Get data for each stock
    stock_data_1 = get_stock_data(stock_code_1, start_date, end_date)
    stock_data_2 = get_stock_data(stock_code_2, start_date, end_date)
    stock_data_3 = get_stock_data(stock_code_3, start_date, end_date)

    # Combine stock data into a single DataFrame
    combined_data = pd.concat(
        [stock_data_1["Close"], stock_data_2["Close"], stock_data_3["Close"]],
        axis=1
    )
    combined_data.columns = [stock_name_1, stock_name_2, stock_name_3]
    combined_data.reset_index(inplace=True)  # Reset index to keep Date as a separate column

    # Calculate average daily changes for each stock
    avg_daily_changes = calculate_daily_changes(combined_data).mean()

    # Calculate the overall average daily change for all stocks
    overall_avg_daily_change = avg_daily_changes.mean()

    # Create a DataFrame to display the average daily changes
    avg_daily_changes_df = pd.DataFrame({'Average Daily Change (%)': avg_daily_changes.round(2)})

    # Add a row for the overall average daily change
    avg_daily_changes_df.loc['Overall'] = overall_avg_daily_change.round(2)

    # Display the average daily changes in a table
    st.subheader("Average Daily Changes (%)")
    st.table(avg_daily_changes_df)

    # Calculate ROI for each stock
    roi_1 = calculate_roi(stock_data_1)
    roi_2 = calculate_roi(stock_data_2)
    roi_3 = calculate_roi(stock_data_3)

    # Plot the closing prices using Altair
    st.subheader("Closing Prices")
    chart = alt.Chart(combined_data.melt('Date', var_name='Company', value_name='Closing Price')).mark_line().encode(
        x='Date:T',
        y='Closing Price:Q',
        color='Company:N'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)


    # Display the average daily changes in a table
    st.subheader("Average Daily Changes (%)")
    avg_daily_changes_rounded = avg_daily_changes.round(2)
    st.table(avg_daily_changes_rounded)

    # Display the ROI for each stock in a table
    st.subheader("Return on Investment (ROI) for Investment Time Interval")
    roi_data = {
        'Stock': [stock_name_1, stock_name_2, stock_name_3],
        'ROI (%)': [roi_1, roi_2, roi_3]
    }
    roi_table = pd.DataFrame(roi_data)
    roi_table = roi_table.set_index('Stock')
    roi_table['ROI (%)'] = roi_table['ROI (%)'].round(2).astype(str) + '%'
    st.table(roi_table)

    # Calculate dividend yield for each stock
    dividend_yield_1 = calculate_dividend_yield(stock_code_1, start_date, end_date)
    dividend_yield_2 = calculate_dividend_yield(stock_code_2, start_date, end_date)
    dividend_yield_3 = calculate_dividend_yield(stock_code_3, start_date, end_date)

    # ... (The rest of the code remains unchanged)

    # Display the year-on-year dividend yield for each stock in a table
    st.subheader("Year-on-Year Dividend Yield (%)")
    dividend_yield_data = {
        'Stock': [stock_name_1, stock_name_2, stock_name_3],
        'Dividend Yield (%)': [dividend_yield_1, dividend_yield_2, dividend_yield_3]
    }
    dividend_yield_table = pd.DataFrame(dividend_yield_data)
    dividend_yield_table = dividend_yield_table.set_index('Stock')
    dividend_yield_table['Dividend Yield (%)'] = dividend_yield_table['Dividend Yield (%)'].round(2).astype(str) + '%'
    st.table(dividend_yield_table)


if __name__ == "__main__":
    main()
