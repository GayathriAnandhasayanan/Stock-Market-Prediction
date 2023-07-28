import requests

data_to_insert = [
    {
        "stock_code": "AAPL",
        "prediction_date": "2023-08-01",
        "predicted_value": 150.0,
        "predicted_date": "2023-08-02",
    },
    {
        "stock_code": "GOOG",
        "prediction_date": "2023-07-01",
        "predicted_value": 120.0,
        "predicted_date": "2023-07-02",
    },
    # Add more data here
]

response = requests.post("http://localhost:8000/stocks/insert_data/", json=data_to_insert)
print(response.json())
