import pandas as pd

def cv_folds_author(X):

    df = pd.DataFrame(data=[data.__dict__ for data in X])

    for author in df['author'].unique():
        train_idx = df.loc[df['author'] != author].index.values.tolist()
        valid_idx = df.loc[df['author'] == author].index.values.tolist()
        yield train_idx, valid_idx