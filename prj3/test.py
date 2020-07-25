from IPython.core.display import display, HTML

from confusion_matrix import plot_confusion_matrix_from_data
from data import load_database_test, load_database_train

def test_model(model, train=True):

    train_data = load_database_train()
    test_data = load_database_test()

    if train:
        model.fit(train_data.get_datalist(), train_data.get_y())

    display(HTML('<h5>Gráfico Teste Final: </h5>'))
    predictions = model.predict(test_data.get_datalist())
    plot_confusion_matrix_from_data(test_data.get_y(), predictions)