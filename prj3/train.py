import sys

from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

from confusion_matrix import plot_confusion_matrix_from_data
from cross_validation import cv_folds_author

def grid_search(model, param_grid, X, y, n_jobs=6):

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

    cv = list(cv_folds_author(X))

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
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(df.index, df['mean_train_score'], marker='o', color="blue")
    ax.errorbar(df.index, df['mean_test_score'], yerr=df['std_test_score'], fmt='rD', ecolor="red", label="Test")
    ax.set_xticks(df.index)

    ax.legend(["Treino", "Validação"])
    ax.set_xlabel('Número do experimento')
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

