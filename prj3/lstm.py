from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, LSTM
from tensorflow.python.keras.wrappers.scikit_learn import KerasClassifier

# Create function returning a compiled network
from cross_validation import cv_folds_author
from data import load_database_train
from preprocessing import InterpolateRawData

database_train = load_database_train()



def create_network():
    model = Sequential()

    model.add(LSTM(256, input_shape=(600,)))

    model.add(Dense(units=10, activation='relu'))

    model.add(Dense(6, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

# Wrap Keras model so it can be used by scikit-learn
neural_network = KerasClassifier(build_fn=create_network,
                                 epochs=10,
                                 batch_size=100,
                                 verbose=0)


pipe = Pipeline([
    ('interpolate', InterpolateRawData(num_samples=100)),
    ('neural_network', neural_network)])

print(cross_val_score(pipe, database_train.X, database_train.y, cv=cv_folds_author(database_train.X)))

print(InterpolateRawData(num_samples=50).fit_transform(database_train.X)[0].shape)
print(database_train.y.shape)