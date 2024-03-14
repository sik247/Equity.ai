import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
#from lstm_model_manager import create_and_train_lstm_model  # Assuming lstm_model_manager.py contains LSTM model functions


def create_lstm_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)  # Predicting a single value
    ])
    return model

def create_and_train_lstm_model(X_train, y_train, learning_rate=0.001, epochs=100, batch_size=32):
    model = create_lstm_model((X_train.shape[1], X_train.shape[2]))
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    
    # Fit model
    model_history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model, model_history

# Adjusted handler function name to be more descriptive
def handle_lstm_prediction(stock_data, parameters):
    # Assuming stock_data has been preprocessed to create X_train, y_train
    
    # Extract parameters
    learning_rate = parameters.get('learning_rate', 0.001)
    epochs = parameters.get('epochs', 100)
    batch_size = parameters.get('batch_size', 32)
    
    # Train model
    model, model_history = create_and_train_lstm_model(X_train, y_train, learning_rate, epochs, batch_size)
    
    # After training, you can save the model, predict, or further process the output
    
    # For the sake of example, let's return the training history's loss values
    return model_history.history['loss']
