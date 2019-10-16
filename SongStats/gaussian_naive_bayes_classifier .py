import numpy as np
import pandas as pd
import csv
import itertools
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# import dataset
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'

log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

locations_eastwest = log_song_data_unique.drop(log_song_data_unique.loc[log_song_data_unique['Region'].isin(['mid',
                     'south'])].index).copy().reset_index(drop=True)[['Latitude', 'Longitude']]
locations_mid = log_song_data_unique.loc[log_song_data_unique['Region'].isin(['mid'])].copy().reset_index(drop=True)[
                ['Latitude', 'Longitude']]

col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay',
               'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# get mid data separately
data_mid = data_subset.loc[data_subset['Region'].isin(['mid'])].copy().reset_index(drop=True)

# use only east and west data
data = data_subset.drop(data_subset.loc[data_subset['Region'].isin(['mid', 'south'])].index).copy().reset_index(
    drop=True)

data_rounded = data.round({'Latitude': 2, 'Longitude': 2})

'''
set up labels --> the categories we want to be able to sort the data into and their actual category
'''
label_names = data.Region.unique()
labels = pd.get_dummies(data.Region, drop_first=True).values.ravel()

'''
all 16 song variables
'''
# organizing data into sets
feature_names = data.columns[3:].values
features = data.loc[:, data.columns[3:]].values

train, test, train_labels, test_labels = train_test_split(features,
                                                          labels,
                                                          test_size=0.33,
                                                          random_state=42)

# initialize our classifier
gnb = GaussianNB()

# train our classifier
model = gnb.fit(train, train_labels)

# make predictions
preds = gnb.predict(test)

# evaluate accuracy
prediction = {'all 16 variables': accuracy_score(test_labels, preds)}
print(accuracy_score(test_labels, preds))
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions'
          '/MachineLearningClassifier'
          '/allVariablesTogether.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in sorted(prediction.items(), key=lambda kv: kv[1], reverse=True):
       writer.writerow([key, value])


'''
all individual variables
'''
# organizing data into sets
predictions = dict()
for i in data.columns[3:].values:

    feature_name = i
    feature = data.loc[:, data.columns == i].values

    train, test, train_labels, test_labels = train_test_split(feature,
                                                              labels,
                                                              test_size=0.33,
                                                              random_state=42)

    # initialize our classifier
    gnb = GaussianNB()

    # train our classifier
    model = gnb.fit(train, train_labels)

    # make predictions
    preds = gnb.predict(test)

    # evaluate accuracy
    predictions[feature_name] = accuracy_score(test_labels, preds)
    # print(feature_name, accuracy_score(test_labels, preds))
print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions'
          '/MachineLearningClassifier'
          '/allIndividuals.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
       writer.writerow([key, value])

'''
all combinations of 2 of the 16 song variables
'''
# organizing data into sets
predictions = dict()
combinations = list(itertools.combinations(data.columns[3:].values, 2))
for i in combinations:

    two_feature_names = np.asarray(i)
    two_features = data.loc[:, two_feature_names].values

    train, test, train_labels, test_labels = train_test_split(two_features,
                                                              labels,
                                                              test_size=0.33,
                                                              random_state=42)

    # initialize our classifier
    gnb = GaussianNB()

    # train our classifier
    model = gnb.fit(train, train_labels)

    # make predictions
    preds = gnb.predict(test)

    # evaluate accuracy
    predictions[i] = accuracy_score(test_labels, preds)
    # print(feature_name, accuracy_score(test_labels, preds))
print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions'
          '/MachineLearningClassifier'
          '/combosOfTwo.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
       writer.writerow([key, value])

'''
all combinations of 3 of the 16 song variables
'''
# organizing data into sets
predictions = dict()
combinations = list(itertools.combinations(data.columns[3:].values, 3))
for i in combinations:

    three_feature_names = np.asarray(i)
    three_features = data.loc[:, three_feature_names].values

    train, test, train_labels, test_labels = train_test_split(three_features,
                                                              labels,
                                                              test_size=0.33,
                                                              random_state=42)

    # initialize our classifier
    gnb = GaussianNB()

    # train our classifier
    model = gnb.fit(train, train_labels)

    # make predictions
    preds = gnb.predict(test)

    # evaluate accuracy
    predictions[i] = accuracy_score(test_labels, preds)
    # print(feature_name, accuracy_score(test_labels, preds))
print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions'
          '/MachineLearningClassifier'
          '/combosOfThree.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
       writer.writerow([key, value])

"""
Classifiers using downsampled data by location
"""
# load in list of random seeds
seed_list = np.genfromtxt('C:/Users/abiga\Box '
                          'Sync\Abigail_Nicole\ChippiesProject'
                          '\FinalDataCompilation\RandomSeeds.csv',
                          delimiter=',', dtype='int')

all_variables = pd.DataFrame(index=range(1000),
                             columns=['all_16_variables'])

all_individual = pd.DataFrame(index=range(1000),
                              columns=[data_rounded.columns[3:]])

combinations_2 = list(itertools.combinations(data_rounded.columns[
                                             3:].values, 2))
combosOfTwo = pd.DataFrame(index=range(1000),
                           columns=[combinations_2])

combinations_3 = list(itertools.combinations(data_rounded.columns[
                                             3:].values, 3))
combosOfThree = pd.DataFrame(index=range(1000),
                             columns=[combinations_3])


for r, seed in zip(range(1000), seed_list):
    sample = data_rounded.groupby(['Latitude', 'Longitude']).apply(
        lambda x: x.sample(1, random_state=seed)).reset_index(drop=True)

    '''
    set up labels --> the categories we want to be able to sort the data 
    into and their actual category
    '''
    label_names = sample.Region.unique()
    labels = pd.get_dummies(sample.Region, drop_first=True).values.ravel()

    '''
    all 16 song variables
    '''
    # organizing data into sets
    feature_names = sample.columns[3:].values
    features = sample.loc[:, sample.columns[3:]].values

    train, test, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.33, random_state=42)

    # initialize our classifier
    gnb = GaussianNB()

    # train our classifier
    model = gnb.fit(train, train_labels)

    # make predictions
    preds = gnb.predict(test)

    # evaluate accuracy
    all_variables.iloc[r]['all_16_variables'] = accuracy_score(test_labels,
                                                               preds)

    '''
    all individual variables
    '''
    # organizing data into sets
    for i in sample.columns[3:].values:

        feature_name = i
        feature = sample.loc[:, sample.columns == i].values

        train, test, train_labels, test_labels = train_test_split(
            feature, labels, test_size=0.33, random_state=42)

        # initialize our classifier
        gnb = GaussianNB()

        # train our classifier
        model = gnb.fit(train, train_labels)

        # make predictions
        preds = gnb.predict(test)

        # evaluate accuracy
        all_individual.iloc[r][feature_name] = accuracy_score(test_labels,
                                                              preds)
    '''
    all combinations of 2 of the 16 song variables
    '''
    # organizing data into sets
    for i in combinations_2:

        two_feature_names = np.asarray(i)
        two_features = sample.loc[:, two_feature_names].values

        train, test, train_labels, test_labels = train_test_split(
            two_features, labels, test_size=0.33, random_state=42)

        # initialize our classifier
        gnb = GaussianNB()

        # train our classifier
        model = gnb.fit(train, train_labels)

        # make predictions
        preds = gnb.predict(test)

        # evaluate accuracy
        combosOfTwo.iloc[r][i] = accuracy_score(test_labels, preds)

    '''
    all combinations of 3 of the 16 song variables
    '''
    # organizing data into sets
    for i in combinations_3:

        three_feature_names = np.asarray(i)
        three_features = sample.loc[:, three_feature_names].values

        train, test, train_labels, test_labels = train_test_split(
            three_features, labels, test_size=0.33, random_state=42)

        # initialize our classifier
        gnb = GaussianNB()

        # train our classifier
        model = gnb.fit(train, train_labels)

        # make predictions
        preds = gnb.predict(test)

        # evaluate accuracy
        combosOfThree.iloc[r][i] = accuracy_score(test_labels, preds)

downsampling_all = pd.concat([all_variables.max(axis=0),
                              all_variables.min(axis=0)],
                             axis=1,
                             keys=['all_variables_max',
                                   'all_variables_min'])
downsampling_all.to_csv('C:/Users/abiga/Box '
                        'Sync/Abigail_Nicole/ChippiesProject'
                        '/StatsOfFinalData_withReChipperReExported'
                        '/AnimalBehaviourRevisions'
                        '/MachineLearningClassifier'
                        '/allVariablesTogether_downsampled.csv')

downsampling_individual = pd.concat([all_individual.max(axis=0),
                                     all_individual.min(axis=0)],
                                    axis=1,
                                    keys=['all_individuals_max',
                                          'all_individuals_min'])
downsampling_individual.to_csv('C:/Users/abiga/Box '
                               'Sync/Abigail_Nicole/ChippiesProject'
                               '/StatsOfFinalData_withReChipperReExported'
                               '/AnimalBehaviourRevisions'
                               '/MachineLearningClassifier'
                               '/allIndividuals_downsampled.csv')

downsampling_combosTwo = pd.concat([combosOfTwo.max(axis=0),
                                    combosOfTwo.min(axis=0)],
                                   axis=1,
                                   keys=['combosTwo_max',
                                         'combosTwo_min'])
downsampling_combosTwo.to_csv('C:/Users/abiga/Box '
                              'Sync/Abigail_Nicole/ChippiesProject'
                              '/StatsOfFinalData_withReChipperReExported'
                              '/AnimalBehaviourRevisions'
                              '/MachineLearningClassifier'
                              '/combosOfTwo_downsampled.csv')

downsampling_combosThree = pd.concat([combosOfThree.max(axis=0),
                                      combosOfThree.min(axis=0)],
                                     axis=1,
                                     keys=['combosThree_max',
                                           'combosThree_min'])
downsampling_combosThree.to_csv('C:/Users/abiga/Box '
                                'Sync/Abigail_Nicole/ChippiesProject'
                                '/StatsOfFinalData_withReChipperReExported'
                                '/AnimalBehaviourRevisions'
                                '/MachineLearningClassifier'
                                '/combosOfThree_downsampled.csv')

