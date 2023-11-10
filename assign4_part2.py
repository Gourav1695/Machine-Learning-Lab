# -*- coding: utf-8 -*-
"""assign4_part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eunghGYKEvurqprEgEqBTgjMmIc-L6IE

# Assignment 4 Part 2


Name: Gourav Kumar Shaw

Enrolment Number: 2020CSB010

Machine Learning Lab

## Task 6

Download the Forest Cover Type dataset (https://www.kaggle.com/uciml/forest-cover-type-dataset) and pre-process the dummy variables to create training, test, and development set. Reduce the train data size if the system unable to process the whole dataset.
"""

import pandas as pd

_FILE_PATH = '/content/drive/MyDrive/ML_DRIVE/Assign_3/covtype.csv'

cov_df = pd.read_csv(_FILE_PATH)

cov_df

from google.colab import drive
drive.mount('/content/drive')

cov_df.columns

from sklearn.preprocessing import StandardScaler

def standardize(df: "pd.DataFrame", col_name: "str") -> "pd.DataFrame":
    scaler = StandardScaler()

    df[[col_name]] = pd.DataFrame(
        data=scaler.fit_transform(df[[col_name]]),
        index=df.index,
        columns=[col_name]
    )
    return df

_columns_to_scale = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
                    'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
                    'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
                    'Horizontal_Distance_To_Fire_Points']

for _col in _columns_to_scale:
    cov_df = standardize(cov_df, _col)

cov_df

cov_df[['Cover_Type']].value_counts()

# NOTE: class imbalance is present but removing it will
# remove the data that cover_type 2 is the most common data in world

cov_df = cov_df.sample(frac=0.1)

X = cov_df.drop('Cover_Type', axis=1)
y = cov_df[['Cover_Type']]

y.value_counts()

# 80% as train
# 10% as validation
# 10% as train

from sklearn.model_selection import train_test_split

X_train, _X_rest, y_train, _y_rest = train_test_split(X, y, train_size=0.8)
X_val, X_val, y_val, y_val = train_test_split(_X_rest, _y_rest, train_size=0.5)

"""## Task 7

Train the one vs rest and one-vs-one SVM model on the above dataset for
multiclass classification. Plot and Analyze the Confusion matrix for the above models. Show the accuracy in the graph. State the difference of the two approaches using the model parameters.
"""

# hyper parameter tuning

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def display_confusion_matrix(X_test: "pd.DataFrame",
                             y_test: "pd.DataFrame",
                             model: "SVC"):
    y_predict = model.predict(X_test)
    matrix = confusion_matrix(y_test, y_predict)
    fig = plt.figure(figsize=(10,10))
    sns.heatmap(
        matrix,
        xticklabels=range(1,8),
        yticklabels=range(1,8),
        linewidth=0.5,
        cmap='coolwarm',
        annot=True,
        cbar=True,
        square=True)
    plt.title('HeatMap for the model')
    plt.ylabel('Actual Value')
    plt.xlabel('Predicted Value')
    plt.show()

decision_function_shapes = ['ovo', 'ovr']

models = [
    SVC(decision_function_shape=shape).fit(X_train, y_train.iloc[:, 0])
    for shape in decision_function_shapes
]

# Accuracies

accuracies = [model.score(X_val, y_val) for model in models]


print(pd.DataFrame(columns=['decision_function_shape', 'Accuracy'],
             data=zip(decision_function_shapes, accuracies)))

plt.bar(range(0, len(accuracies)), accuracies)
plt.title('OvO vs OvR Accuracy')
plt.ylabel('Accuracy')
plt.xticks(ticks=[0,1], labels=['ovo', 'ovr'])
plt.show()

for model in models:
    display_confusion_matrix(X_val, y_val, model)