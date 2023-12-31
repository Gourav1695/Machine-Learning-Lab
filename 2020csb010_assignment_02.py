# -*- coding: utf-8 -*-
"""2020CSB010_assignment_02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19jVPkC5OCf5dR0pZx1hLcpVEUaU0Dtu9

# Assignment 2

- Name: **GOURAV KUMAR SHAW**
- Roll: **2020CSBO1O**

## (i) Download data

Data downloaded.
"""

from google.colab import drive
drive.mount('/content/drive')

BASE_PATH = '/content/drive/MyDrive/ML_DRIVE/Assign_2'

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.naive_bayes import BernoulliNB
from random import randint
from statistics import mean
import matplotlib.pyplot as plt

dataset = pd.read_csv(f"{BASE_PATH}/data.csv")
print("Dataset shape:", dataset.shape)
print("Dataset columns:", dataset.columns)

dataset = dataset.drop(columns = ['id', 'Unnamed: 32'])
dataset

"""## (ii) Implement Logistic regression
Implement Logistic regression using scikit-learn package in python after splitting the dataset 80:10:10 percent (use seed = 5 for splitting).
"""

def train_validate_test_split(df, train_percent=.8, validate_percent=.1, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, validate, test

train_df, validation_df, test_df = train_validate_test_split(dataset, train_percent=0.8, validate_percent=0.1, seed=5)
print("Shape of train:", train_df.shape)
print("Shape of validation:", validation_df.shape)
print("Shape of test:", test_df.shape)

train_df

validation_df

test_df

y_test, y_train, y_valid = test_df['diagnosis'], train_df['diagnosis'], validation_df['diagnosis']
X_test, X_train, X_valid = test_df.drop('diagnosis', axis=1), train_df.drop('diagnosis', axis=1), validation_df.drop('diagnosis', axis=1)

"""## (iii) Train Logistic Regression Model"""

def train_model_with_solver(X_train, y_train, X_valid, y_valid, solver, penalty='l2', C=1.0):
  lr = LogisticRegression(solver = solver, max_iter = 10000, penalty=penalty, C=C)
  lr.fit(X_train, y_train)
  score = lr.score(X_valid, y_valid)

  return {
      "solver": solver,
      "score": score,
      "coefs": lr.coef_.tolist()[0],
      "penalty": penalty,
      "inv_of_regularization": C
  }

def display_table(models, columns):
  headers = ['solver', 'accuracy', 'penalty', 'inv_of_regularization'] + columns.tolist()
  data = [[model['solver'], model['score'], model["penalty"], model["inv_of_regularization"]] + model['coefs'] for model in models]

  return pd.DataFrame(
      columns = headers,
      data = data
  )

newton_cg_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "newton-cg")
lbfgs_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "lbfgs")
liblinear_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "liblinear")

display_table([newton_cg_model, lbfgs_model, liblinear_model], X_train.columns)

"""## (iv) Use ‘l1’, ‘l2’, ‘none’ penality to train the Logistic regression model."""

l1_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "saga", penalty="l1")
l2_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "saga", penalty="l2")
none_model = train_model_with_solver(X_train, y_train, X_valid, y_valid, "saga", penalty="none")

display_table([l1_model, l2_model, none_model], X_train.columns)

"""## (v) Vary the l1 penalty over the range (0.1, 0.25, 0.75, 0.9)
compare the coefficients of the features.
"""

penalties = [1e-6,0.1, 0.25, 0.75, 0.9]
models = [train_model_with_solver(X_train, y_train, X_valid, y_valid, "saga", penalty="l1", C=p) for p in penalties]
display_table(models, X_train.columns)

"""## (vi) Estimate the average accuracy of the Naive Bayes algorithm using 5-fold cross-validation
Use scikit-learn package in python. Plot the bar graph using matplotlib.
"""

X = dataset.drop('diagnosis', axis=1)
y = dataset['diagnosis']
folds = KFold(n_splits=5, shuffle=True)
nb_accuracy = []
for train_ids, test_ids in folds.split(X):
  X_train = X.iloc[train_ids]
  y_train = y.iloc[train_ids]
  X_test = X.iloc[test_ids]
  y_test = y.iloc[test_ids]

  naive_bayes_model = BernoulliNB()
  naive_bayes_model.fit(X_train, y_train)

  accuracy = naive_bayes_model.score(X_test, y_test)
  nb_accuracy.append(accuracy)

print("Avg accuracy = ", mean(nb_accuracy))

plt.xlabel('5-Fold Iteration')
plt.ylabel('Accuracy')
plt.title('Accuracy of the 5-Fold Iterations')
plt.bar([x for x in range(1,6)],nb_accuracy, color='green')
plt.plot()

