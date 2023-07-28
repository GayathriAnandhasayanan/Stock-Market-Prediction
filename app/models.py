# app/models.py

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class PredictionData:
    def __init__(self, stock_code, prediction_date, predicted_value, predicted_date):
        self.stock_code = stock_code
        self.prediction_date = prediction_date
        self.predicted_value = predicted_value
        self.predicted_date = predicted_date
