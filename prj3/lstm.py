from tensorflow.python.keras import Sequential
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Dense, LSTM, Masking
from tensorflow.python.keras.optimizer_v2.adam import Adam
from tensorflow.python.keras.regularizers import l2

from data import load_database_train
from preprocessing import InterpolateRawData
from train import keras_train_and_validate

database_train = load_database_train()

def create_network():
    model = Sequential()
    model.add(Masking(mask_value=0, input_shape=(None, 6)))
    model.add(LSTM(50, activation='sigmoid', input_shape=(None, 6), activity_regularizer=l2(0.00001)))
    #model.add(Dense(20, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
    return model


X = InterpolateRawData(num_samples=50,flatten_data=False).fit_transform(database_train.X)

keras_train_and_validate(create_network(), X, database_train.y_encoded,
                         database_train.cv_author, database_train.decode, epochs=1000, batch_size=100,
                         callbacks=EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=50))