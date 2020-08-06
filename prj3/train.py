import sys

from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

from confusion_matrix import plot_confusion_matrix_from_data

def grid_search(model, param_grid, X, y, cv, n_jobs=6, figsize=(10, 10)):
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

    grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, scoring='accuracy',
                        return_train_score=True, verbose=10, n_jobs=n_jobs, refit=False)
    grid.fit(X, y)
    sys.stdout.flush()

    # Coloca dados em uma tabela pandas e exibe
    display(HTML('<h3>Relatório dos experimentos: </h3>'))
    cv_results = grid.cv_results_
    df = pd.DataFrame(cv_results)
    df = df[['params', 'mean_train_score', 'std_train_score', 'mean_test_score', 'std_test_score']]
    pd.options.display.float_format = '{:.2f}'.format
    display(df)

    # Grafico Acuracia dos experimentos grid search
    display(HTML('<h3>Gráfico dos experimentos: </h3>'))
    fig, ax = plt.subplots(figsize=figsize)

    if isinstance(param_grid, dict) and len(param_grid.keys()) == 1:
        key = list(param_grid.keys())[0]
        index = [str(p) for p in param_grid[key]]
        ax.set_xlabel('Valor de {}'.format(key))
    else:
        index = df.index
        ax.set_xlabel('Número do experimento')

    ax.scatter(index, df['mean_train_score'], marker='o', color="blue")
    ax.errorbar(index, df['mean_test_score'], yerr=df['std_test_score'], fmt='rD', ecolor="red", label="Test")
    ax.set_xticks(index)

    ax.legend(["Treino", "Validação"])
    ax.set_ylabel('Acurácia')
    plt.show()

    # Printa melhor modelo (linha da tabela)
    display(HTML('<h3>Melhor Modelo: </h3>'))
    display(df.loc[[grid.best_index_]])

    # Retreina melhor modelo com validacao
    model.set_params(**grid.best_params_)

    val_predicts = []
    val_targets = []

    for train_index, val_index in cv:
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        model.fit(X_train, y_train)

        val_predicts.extend(model.predict(X_val))
        val_targets.extend(y_val)

    display(HTML('<h5>Gráfico Matriz de Confusão: </h5>'))

    pd.reset_option('display.max_colwidth', silent=True)

    plot_confusion_matrix_from_data(val_targets, val_predicts, np.unique(np.array(val_targets)))

    return model


def scikit_train_validate(model, X, y, cv):

    val_predicts = []
    val_targets = []

    scores_train = []
    scores_val = []

    for train_index, val_index in cv:
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        model.fit(X_train, y_train)

        scores_train.append(accuracy_score(y_train, model.predict(X_train)))
        scores_val.append(accuracy_score(y_val, model.predict(X_val)))

        val_predicts.extend(model.predict(X_val))
        val_targets.extend(y_val)

    print('train_scores:     {} '.format(["{:.2f}".format(score) for score in scores_train]))
    print('mean_train_score: {:.2f}'.format(np.mean(scores_train)))
    print('std_train_score:  {:.2f}\n\n'.format(np.std(scores_train)))
    print('test_scores:      {}'.format(["{:.2f}".format(score) for score in scores_val]))
    print('mean_test_score:  {:.2f}'.format(np.mean(scores_val)))
    print('std_test_score:   {:.2f}'.format(np.std(scores_val)))

    display(HTML('<h5>Gráfico Matriz de Confusão: </h5>'))
    pd.reset_option('display.max_colwidth', silent=True)
    plot_confusion_matrix_from_data(val_targets, val_predicts, np.unique(np.array(val_targets)))


def keras_train_and_validate(model, X, y, cv, decoder, epochs=10, batch_size=None, callbacks=None):

    val_predicts = []
    val_targets = []

    scores_train = []
    scores_val = []

    Wsave = model.get_weights()

    for train_index, val_index in cv:
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        bs = batch_size
        if bs is None:
            bs = len(X_train)

        model.set_weights(Wsave)
        model.fit(X_train, y_train, epochs=epochs, batch_size=bs, validation_data=(X_val, y_val),
                  callbacks=callbacks, verbose=1)

        pred_val = decoder(model.predict(X_val))
        target_val = decoder(y_val)
        pred_train = decoder(model.predict(X_train))
        target_train = decoder(y_train)

        scores_train.append(accuracy_score(target_train, pred_train))
        scores_val.append(accuracy_score(target_val, pred_val))

        val_predicts.extend(pred_val)
        val_targets.extend(target_val)

    print('train_scores:     {} '.format(["{:.2f}".format(score) for score in scores_train]))
    print('mean_train_score: {:.2f}'.format(np.mean(scores_train)))
    print('std_train_score:  {:.2f}\n\n'.format(np.std(scores_train)))
    print('test_scores:      {}'.format(["{:.2f}".format(score) for score in scores_val]))
    print('mean_test_score:  {:.2f}'.format(np.mean(scores_val)))
    print('std_test_score:   {:.2f}'.format(np.std(scores_val)))

    display(HTML('<h5>Gráfico Matriz de Confusão: </h5>'))
    pd.reset_option('display.max_colwidth', silent=True)
    plot_confusion_matrix_from_data(val_targets, val_predicts, np.unique(np.array(val_targets)))
