from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


from data import load_train
from preprocessing import InterpolateRawData

database_train = load_train()

pipe = Pipeline([
    ('interpolate', InterpolateRawData(num_samples=10)),
    ('knn', LogisticRegression(random_state=0, max_iter=100000))
])

#pipe.fit(database_train.get_datalist(), database_train.get_y())

scores = cross_val_score(pipe, database_train.get_datalist(), database_train.get_y(), cv=10)
print(scores)