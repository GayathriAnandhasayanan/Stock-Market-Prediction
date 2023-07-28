import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import yfinance as yf

from app import TODAY
from app.utils import LOOK_BACKS, SCALER

import plotly.graph_objs as go

def get_data(ticker, start_date='2010-01-01', end_date=TODAY):
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    data = data.drop(columns=['Adj Close'])

    return data


def normalized_split_data(data: pd.DataFrame, features: list[str], is_evalute=False):
    # Choose only Close price of stock
    dataset = data.filter(features).values

    # Scale our data from 0 to 1
    if is_evalute:
        joblib.load('./models/NFLX_SCALER.joblib')
        scaled_data = SCALER.transform(dataset)
    else:
        scaled_data = SCALER.fit_transform(dataset)
        joblib.dump(SCALER, './models/NFLX_SCALER.joblib')

    # Train data - 80%, test - 20%
    training_data_len = int(np.ceil(len(dataset) * 0.80))

    # Use our scaled data for training
    x_train, y_train = [], []

    for i in range(LOOK_BACKS, len(scaled_data)):
        x_train.append(scaled_data[i - LOOK_BACKS:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape input data for LSTM
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    if is_evalute:
        print(x_train.shape, y_train.shape)
        return x_train, y_train

    # print(x_train.shape, y_train.shape)
    # return x_train, y_train

    # # Create test dataset
    test_data = scaled_data[training_data_len - LOOK_BACKS:, :]
    x_test = [test_data[i - LOOK_BACKS:i, 0] for i in range(LOOK_BACKS, len(test_data))]
    x_test = np.array(x_test).reshape(-1, LOOK_BACKS, 1)
    y_test = dataset[training_data_len:, :]

    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
    return x_train, y_train, x_test, y_test


def train_model(x_train, y_train, model_name):
    tf.keras.backend.clear_session()

    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(x_train.shape[1], 1)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=False)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(25, activation='relu'),
        tf.keras.layers.Dense(1),
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    # Тrain the model
    model.fit(x_train, y_train,
              batch_size=1,
              epochs=11,
              use_multiprocessing=True)

    model.save(f'./model/{model_name}.h5')

    return {'message': f'model {model_name} trained successfully',
            'status': 200}


def make_prediction(input_data, model):
    def do_prediction(data, model):
        def predict(num_prediction, model):
            prediction_list = close_data[-LOOK_BACKS:]

            for _ in range(num_prediction):
                x = prediction_list[-LOOK_BACKS:]
                x_scaled = scaler.transform(x.reshape(-1, 1))
                x_scaled = x_scaled.reshape((1, LOOK_BACKS, 1))
                out = model.predict(x_scaled)[0][0]
                prediction_list = np.append(prediction_list, scaler.inverse_transform(out.reshape(-1, 1)))
            prediction_list = prediction_list[LOOK_BACKS - 1:]

            return prediction_list

        def predict_dates(num_prediction):
            last_date = data.index.values[-1]
            prediction_dates = pd.date_range(last_date, periods=num_prediction + 1).tolist()
            return prediction_dates

        close_data = data.Close.values.reshape((-1))

        num_prediction = 15
        forecast = predict(num_prediction, model)
        forecast_dates = predict_dates(num_prediction)

        result = pd.concat([pd.DataFrame(forecast_dates), pd.DataFrame(forecast)], ignore_index=True, axis=1)
        return result.rename({0: 'Date', 1: 'Close'}, axis=1)

    scaler = joblib.load('./models/NFLX_SCALER.joblib')
    loaded_model = tf.keras.models.load_model(f'./models/{model}.h5')
    # Perform any preprocessing of the test_data if needed
    return do_prediction(input_data, loaded_model)

def make_prediction_2(stock_name, start_date, end_date):
    look_back = 60
    loaded_model = tf.keras.models.load_model(f'./models/{stock_name}_LSTM.h5')
    # Predict stock prices for next month
    data_new = yf.download(stock_name, start=start_date, end=end_date)

    data_new = data_new.filter(['Close'])
    dataset = data_new.values
    training_data_len = len(dataset)

    loaded_scaler = joblib.load(f'./models/{stock_name}_SCALER.joblib')
    scaled_data = loaded_scaler.transform(dataset)

    test_data = scaled_data[:, :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(look_back, len(test_data)):
        x_test.append(test_data[i - look_back:i, 0])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    hist_data_new = yf.download(stock_name, start=start_date, end=end_date)
    hist_data_new = hist_data_new.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    hist_data_new = hist_data_new['Close']
    hist_data_new = np.array(hist_data_new)
    pred_lstm = loaded_model.predict(x_test)
    pred_lstm = pred_lstm[:-1]
    pred_lstm = loaded_scaler.inverse_transform(pred_lstm)

    # build graphs
    preds_gr = np.reshape(pred_lstm, (x_test.shape[0] - 1,))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(range(0, x_test.shape[0] - 1)), y=hist_data_new, mode='lines+markers', name='historical',
                   marker_color='#39304A'))
    fig.add_trace(
        go.Scatter(x=list(range(0, x_test.shape[0] - 1)), y=preds_gr, mode='lines+markers', name='predictions',
                   marker_color='#FFAA00'))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      plot_bgcolor='#FFFFFF',
                      xaxis=dict(gridcolor='lightgrey'),
                      yaxis=dict(gridcolor='lightgrey'),
                      title_text=f'{stock_name} LSTM prediction', title_x=0.5,
                      xaxis_title="Timestep",
                      yaxis_title="Stock price",
                      margin=dict(l=0, r=0, t=30, b=0))
    return fig
