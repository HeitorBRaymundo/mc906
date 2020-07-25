import pandas as pd

def cv_folds_author(database):

    df = pd.DataFrame(data=database.to_dict())

    for author in df['author'].unique():
        train_idx = df.loc[df['author'] != author].index.values.tolist()
        valid_idx = df.loc[df['author'] == author].index.values.tolist()
        yield train_idx, valid_idx