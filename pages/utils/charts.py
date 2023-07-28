import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as ms


def candle_bar(data_chart: pd.DataFrame):
    """
    Creates a candlestick chart with volume bars.

    Args:
        data_chart (pd.DataFrame): DataFrame containing the financial data.

    Returns:
        go.Figure: Plotly Figure object representing the candlestick chart.

    """

    # Create a subplot with two rows
    fig = ms.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Add candlestick trace to the first row
    fig.add_trace(
        go.Candlestick(
            x=data_chart.index,
            open=data_chart.Open,
            high=data_chart.High,
            low=data_chart.Low,
            close=data_chart.Close
        )
    )

    # Add volume bars trace to the second row
    fig.add_trace(
        go.Bar(x=data_chart.index, y=data_chart.Volume),
        row=2, col=1
    )

    # Update layout to hide the x-axis range slider
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def line_chart(data_chart: pd.DataFrame, feature='Close'):
    """
    Creates a line chart for a specified feature in the financial data.

    Args:
        data_chart (pd.DataFrame): DataFrame containing the financial data.
        feature (str): Name of the feature column to be plotted (default: 'Close').

    Returns:
        go.Figure: Plotly Figure object representing the line chart.

    """

    # Create a new Figure object
    fig = go.Figure()

    # Add a scatter trace for the specified feature
    fig.add_trace(go.Scatter(x=data_chart.index, y=data_chart[feature], mode='lines', name='Stock Prices'))

    # Update the layout with title and axis labels
    fig.update_layout(
        title='Stock Prices History',
        xaxis=dict(title='Date'),
        yaxis=dict(title=feature)
    )
    return fig


def macd_chart(data_chart: pd.DataFrame):
    # Create a line plot for the 'macd' column
    line_trace = go.Scatter(x=data_chart.index, y=data_chart.MACD_12_26_9, name='MACD')
    Historgram = go.Bar(x=data_chart.index, y=data_chart.MACDh_12_26_9, name='Historgram')
    Signal = go.Scatter(x=data_chart.index, y=data_chart.MACDs_12_26_9, name='Signal')

    # Create the figure and add the traces
    fig = go.Figure(data=[line_trace, Historgram, Signal])

    # Add layout and axis labels
    fig.update_layout(title='Data with MACD', xaxis_title='Index', yaxis_title='Price')

    return fig


def prediction_chart(prediction_data, original_data):
    # Create traces for each DataFrame
    trace1 = go.Scatter(x=prediction_data['Date'], y=prediction_data['Close'], mode='lines+markers', name='Predict')
    trace2 = go.Scatter(x=original_data.index, y=original_data['Close'], mode='lines+markers', name='Original')

    # Create the figure and add the traces
    fig = go.Figure(data=[trace1, trace2])

    # Update the layout for better appearance (optional)
    fig.update_layout(
        title='Stock Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='white',
        xaxis=dict(showline=True, linewidth=1, linecolor='lightgray', mirror=True),
        yaxis=dict(showline=True, linewidth=1, linecolor='lightgray', mirror=True),
    )

    # Show the plot
    return fig
