import socket
import sys

from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, GridSearchCV
import pandas as pd
import numpy as np

def plot_image(*images, titles=[], table_format=(1, 0), figsize=(15, 15), axis=False, fontsize=20):
    '''
    Função auxiliar para comparar diferentes soluções (por imagens)
    '''
    max_lines = table_format[0] if table_format[0] != 0 else len(images)
    max_columns = table_format[1] if table_format[1] != 0 else len(images)

    fig = plt.figure(figsize=figsize)
    for i, image in enumerate(images):
        ax = fig.add_subplot(max_lines, max_columns, i + 1)

        if len(titles) == len(images):
            ax.set_xlabel(titles[i], fontsize=fontsize)

        if axis is False:
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
        ax.imshow(image)
    plt.show()


def print_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("HOST: {}".format(s.getsockname()[0]))
    s.close()

def user_confirmation(message):
    while 1:
        text = input("{} [y/n]: \n".format(message))
        if text == 'y':
            return True
        elif text == 'n':
            return False
        else:
            print("Digite 'y' ou 'n'")


def keras_train_and_validate(model, X, y, epochs=10000, batch_size=None, callbacks=None, cv=3):

    #result = Result("train", "val")

    for train_index, val_index in KFold(cv, shuffle=True).split(X):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        bs = batch_size
        if bs is None:
            bs = len(X_train)

        model.fit(X_train, y_train, epochs=epochs, batch_size=bs, validation_data=(X_val, y_val),
                  callbacks=callbacks, verbose=1)

        #result.add_split("train", model.predict(X_train).flatten(), y_train, train_index)
        #result.add_split("val", model.predict(X_val).flatten(), y_val, val_index)

        #plot_error(result.get_last_split_result("train"), result.get_last_split_result("val"))

    #display(HTML('<h3>Grafico Final: </h3>'))
    #plot_error(result.get_extended_result("train"), result.get_extended_result("val"))

def grid_search(model, param_grid, X, y, X_test=None, y_test=None, cv=5, n_jobs=6):

    grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=KFold(cv, shuffle=True), scoring='neg_mean_squared_error',
                        return_train_score=True, verbose=10, n_jobs=n_jobs, refit=False)
    grid.fit(X, y)
    sys.stdout.flush()

    # Coloca dados em uma tabela pandas e exibe
    display(HTML('<h3>Relatório dos experimentos: </h3>'))
    cv_results = grid.cv_results_
    df = pd.DataFrame(cv_results)
    df = df[['params', 'mean_train_score', 'std_train_score', 'mean_test_score', 'std_test_score']]


    df[['std_train_score', 'std_test_score']] = df[['std_train_score', 'std_test_score']].apply(lambda x: np.sqrt(x))
    df[['mean_train_score', 'mean_test_score']] = df[['mean_train_score', 'mean_test_score']].apply(
        lambda x: np.sqrt(-x))
    pd.options.display.float_format = '{:.2f}'.format
    display(df)

    # Grafico RMSE dos experimentos grid search
    display(HTML('<h3>Gráfico dos experimentos: </h3>'))
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(df.index, df['mean_train_score'], marker='o', color="blue")
    ax.errorbar(df.index, df['mean_test_score'], yerr=df['mean_test_score'], fmt='rD', ecolor="red", label="Test")
    ax.set_xticks(df.index)

    ax.legend(["Treino", "Validação"])
    ax.set_xlabel('Número do experimento')
    ax.set_ylabel('Erro RMSE')
    plt.show()

    # Printa melhor modelo (linha da tabela)
    display(HTML('<h3>Melhor Modelo: </h3>'))
    display(df.loc[[grid.best_index_]])

    # Retreina melhor modelo com validacao
    model.set_params(**grid.best_params_)
    #result = Result("train", "val", "train_full", "test")
    for train_index, val_index in KFold(cv).split(X):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        model.fit(X_train, y_train)

        #result.add_split("train", model.predict(X_train).flatten(), y_train, train_index)
        #result.add_split("val", model.predict(X_val).flatten(), y_val, val_index)

    display(HTML('<h5>Gráfico Validação Cruzada: </h5>'))
    #plot_error(result.get_extended_result("train"), result.get_extended_result("val"))

    if X_test is not None and y_test is not None:
        display(HTML('<h5>Gráfico Teste Final: </h5>'))
        model.fit(X, y)
        #result.add_split("train_full", model.predict(X).flatten(), y)
        #result.add_split("test", model.predict(X_test).flatten(), y_test)
        #plot_error(result.get_extended_result("train_full"), result.get_extended_result("test"))

    #return result
