import datetime

import streamlit as st
from app.utils.modeling import get_data, make_prediction, make_prediction_2
from pages.utils.charts import *

st.set_page_config(page_title='Prediction', page_icon='📈', layout='wide')

ticker = {'Netflix': 'NFLX',
          'Google': 'GOOG',
          'Apple': 'AAPL',
          }

st.subheader('Orginal Data')

option_col1, option_col2, option_col3, option_col4 = st.columns(4)
with option_col1:
    start_date = st.date_input('from', datetime.date(2020, 1, 1))
with option_col2:
    end_date = st.date_input('to', datetime.date.today())
with option_col4:
    option = st.selectbox('Which Stock would you like to demonstrate?', list(ticker.keys()))
    data = get_data(ticker[option], start_date=start_date, end_date=end_date)

#     # prediction_chart(sample_prediction_data, sample_original_data)

st.plotly_chart(candle_bar(data), use_container_width=True)

st.subheader('Predict Data')

# predict_col1, predict_col2 = st.columns([3, 1])
# with predict_col1:
#     result = make_prediction(data, 'bidirectional_LSTM')
#
#     original = get_data(ticker[option], start_date=str(result.iloc[0, 0])[0:10], end_date=str(result.iloc[-1, 0])[0:10])
#     st.plotly_chart(prediction_chart(prediction_data=result, original_data= original), use_container_width=True)
#
# with predict_col2:
#     st.dataframe(result.iloc[-10:,:])


fig = make_prediction_2(ticker[option], start_date=start_date, end_date=end_date)
st.plotly_chart(fig, use_container_width=True)