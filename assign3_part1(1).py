# -*- coding: utf-8 -*-
"""assign3_part1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QqW8qZICKcf-0Kq8XlZXJIWfuK6uDo8_

# Assignment 3 Part 1

### Machine Learning Lab ###

Name: Gourav Kumar Shaw

Roll No.: 2020CSB010

## Task 1
Download Titanic Dataset (https://www.kaggle.com/heptapod/titanic/version/1#) and do initial pre-processing and train a Logistic Regression for the classifier.
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from google.colab import drive

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

FILE_PATH = "/content/drive/MyDrive/ML_DRIVE/Assign_3/train_and_test2.csv"

titanic_df = pd.read_csv(FILE_PATH).dropna()

titanic_df

titanic_df.columns

# all the zero column are not useful (kaggle saying all zero)
# so ignoring them

# also dropping "Passengerid" cause using pandas internal
# 0-index id
cols_to_be_removed = ['Passengerid', 'zero', 'zero.1', 'zero.2', 'zero.3', 'zero.4', 'zero.5', 'zero.6', 'zero.7', 'zero.8', 'zero.9', 'zero.10', 'zero.11', 'zero.12', 'zero.13', 'zero.14', 'zero.15', 'zero.16', 'zero.17', 'zero.18']
titanic_df = titanic_df.drop(cols_to_be_removed, axis=1)
titanic_df.info()

titanic_df.shape

titanic_df.head()

encoded_cols = ["Pclass", "Embarked"]
titanic_df = pd.get_dummies(titanic_df, columns=encoded_cols)
titanic_df.info()

X = titanic_df.drop('2urvived', axis=1)
y = titanic_df['2urvived']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

print(f"Train Dataset Shape: X_train = {X_train.shape} y_train = {y_train.shape}")

print(f"Test Dataset Shape: X_test = {X_test.shape} y_test = {y_test.shape}")

"""
# Task 2


Analyze and control the overfitting by varying the inverse of regularization strength parameter (0.1, 0.25,0.5, 0.75, 0.9) and plot the accuracy graph for the test set."""

def train_model_with_inv_regu(X_train, y_train, X_test, y_test, C=1.0):
  lr = LogisticRegression(max_iter = 10000, C=C)
  lr.fit(X_train, y_train)
  return lr.score(X_test, y_test)

inv_reg = [0.1, 0.25, 0.5, 0.75, 0.9]
accuracy = []

for ir in inv_reg:
  accuracy.append(train_model_with_inv_regu(X_train, y_train, X_test, y_test, ir))

plt.plot(inv_reg, accuracy, '.-')
plt.title("Inverse Regularization vs Accuracy")
plt.xlabel("Inv. Regularization")
plt.ylabel("Accuracy")
plt.show()

"""## Task 3
Using the same dataset train a Decision Tree classifier and vary the maximum depth of the tree to train at least 5 classifiers to analyze the effectiveness.
"""

from sklearn.tree import DecisionTreeClassifier


def classifierHelper(
    X_train,
    y_train,
    X_test,
    y_test,
    max_depth
):

  max_depths = range(1, max_depth+1)
  accuracies = []

  for md in max_depths:
    classifier_model = DecisionTreeClassifier(max_depth=md).fit(X_train, y_train)
    accuracy = classifier_model.score(X_test, y_test)
    accuracies.append(accuracy)

  return [max_depths, accuracies]

result = classifierHelper(X_train, y_train, X_test, y_test, 40)
plt.plot(result[0], result[1], ".-")
plt.title(f"Max Depth upto - {40} vs Accuracy")
plt.xlabel("Max Depth")
plt.ylabel("Accuracy")
plt.show()