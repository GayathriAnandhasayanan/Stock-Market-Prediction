from sklearn.preprocessing import MinMaxScaler

SCALER = MinMaxScaler(feature_range=(0, 1))
LOOK_BACKS = 60