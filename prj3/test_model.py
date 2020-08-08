from IPython.core.display import display, HTML

from confusion_matrix import plot_confusion_matrix_from_data
from data import load_database_test, load_database_train
import numpy as np

def test_model(model, train=True):

    train_data = load_database_train()
    test_data = load_database_test()

    if train:
        model.fit(train_data.X, train_data.y)

    display(HTML('<h5>Matriz Confusão Teste Final: </h5>'))
    predictions = model.predict(test_data.X)
    plot_confusion_matrix_from_data(test_data.y, predictions, np.unique(np.array(test_data.y)))
