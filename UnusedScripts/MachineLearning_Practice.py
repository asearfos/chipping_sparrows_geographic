# # import numpy as np
# # import sklearn
# # from sklearn.datasets import load_breast_cancer
# # from sklearn.model_selection import train_test_split
# # from sklearn.naive_bayes import GaussianNB
# # from sklearn.metrics import accuracy_score
# #
# # # import dataset
# # data = load_breast_cancer()
# #
# # # organizing data into sets
# # label_names = data['target_names']
# # print(label_names)
# # labels = data['target']
# # print(labels)
# # feature_names = data['feature_names']
# # features = data['data']
# # print(type(label_names))
# #
# # train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=42)
# #
# # # initialize our classifier
# # gnb = GaussianNB()
# #
# # # train our classifier
# # model = gnb.fit(train, train_labels)
# #
# # # make predictions
# # preds = gnb.predict(test)
# #
# # # evaluate accuracy
# # print(accuracy_score(test_labels, preds))
#
#
#
# import numpy as np
# import pandas as pd
# import csv
# import itertools
# import sklearn
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import accuracy_score
#
# # import dataset
# data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
#             '/FinalDataframe_CombinedTables_LogTransformed.csv'
# log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)
#
# log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
#     drop=True)
# col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime',
#                'Latitude', 'Longitude']
# data_subset = log_song_data_unique.drop(col_to_skip, axis=1)
#
# # use only east and west data
# data = data_subset.drop(data_subset.loc[data_subset['Region'].isin(['mid', 'south', 'east'])].index).copy().reset_index(
#     drop=True)
#
# ###
# # set up labels --> the categories we want to be able to sort the data into and their actual category
# ###
# label_names = ['east', 'west']
# labels = np.random.choice([0, 1], size=len(data.Region))
#
# # ###
# # # all 16 song variables
# # ###
# # # organizing data into sets
# # feature_names = data.columns[1:].values
# # features = data.loc[:, data.columns != 'Region'].values
# #
# # train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=42)
# #
# # # initialize our classifier
# # gnb = GaussianNB()
# #
# # # train our classifier
# # model = gnb.fit(train, train_labels)
# #
# # # make predictions
# # preds = gnb.predict(test)
# #
# # # evaluate accuracy
# # print(accuracy_score(test_labels, preds))
#
#
#
# # ###
# # # all individual variables
# # ###
# # # organizing data into sets
# # predictions = dict()
# # for i in data.columns[1:].values:
# #
# #     feature_name = i
# #     feature = data.loc[:, data.columns == i].values
# #
# #     train, test, train_labels, test_labels = train_test_split(feature, labels, test_size=0.33, random_state=42)
# #
# #     # initialize our classifier
# #     gnb = GaussianNB()
# #
# #     # train our classifier
# #     model = gnb.fit(train, train_labels)
# #
# #     # make predictions
# #     preds = gnb.predict(test)
# #
# #     # evaluate accuracy
# #     predictions[feature_name] = accuracy_score(test_labels, preds)
# #     # print(feature_name, accuracy_score(test_labels, preds))
# # print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))
#
#
# ###
# # all combinations of 3 of the 16 song variables
# ###
# # organizing data into sets
# predictions = dict()
# combinations = list(itertools.combinations(data.columns[1:].values, 3))
# for i in combinations:
#
#     three_feature_names = np.asarray(i)
#     three_features = data.loc[:, three_feature_names].values
#
#     train, test, train_labels, test_labels = train_test_split(three_features, labels, test_size=0.33, random_state=42)
#
#     # initialize our classifier
#     gnb = GaussianNB()
#
#     # train our classifier
#     model = gnb.fit(train, train_labels)
#
#     # make predictions
#     preds = gnb.predict(test)
#
#     # evaluate accuracy
#     predictions[i] = accuracy_score(test_labels, preds)
#     # print(feature_name, accuracy_score(test_labels, preds))
# print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))
#
# # with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/MachineLearningClassifier'
# #           '/combosOfThree.csv', 'wb') as csv_file:
# #     writer = csv.writer(csv_file)
# #     for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
# #        writer.writerow([key, value])
#
#


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import random

X = list()
y = list()
files = list()

random_state = 42
test_size = 0.9
n = 100

for i in range(n):
    X.append(i)
    y.append(i + random.random())
    files.append('file_{0:02d}.csv'.format(i))

X_train, X_test, y_train, y_test = train_test_split(X,
                                                y,
                                                test_size=test_size,
                                                random_state=random_state)
X_shuffle = shuffle(X, random_state=random_state)
y_shuffle = shuffle(y, random_state=random_state)
file_shuffle = shuffle(files, random_state=random_state)

print(len(X))
print(n*test_size)
print('len of test',len(X_test))
print('len of train', len(X_train))

# print(X_train)
# print(X_shuffle[int(n * test_size):])
# print(y_shuffle[int(n * test_size):])
print(file_shuffle)
print(file_shuffle[int(n * test_size):])
# print(X_train == X_shuffle[int(n * test_size):])
print(file_shuffle[-len(X_test):])
print(len(file_shuffle[int(n*test_size):]))