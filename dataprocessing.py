import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Dropout

# Assuming X_train is your input features and y_train are the prices you're trying to predict
# X_train shape should be [samples, time steps, features]

model = Sequential()
model.add(SimpleRNN(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(SimpleRNN(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # Predicting a single value

model.compile(optimizer='adam', loss='mean_squared_error')

# Fit model
model.fit(X_train, y_train, epochs=100, batch_size=32)
