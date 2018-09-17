import numpy as np
import pandas as pd
import csv
import itertools
import sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from mpl_toolkits.basemap import Basemap

# import dataset
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

locations_eastwest = log_song_data_unique.drop(log_song_data_unique.loc[log_song_data_unique['Region'].isin(['mid',
                     'south'])].index).copy().reset_index(drop=True)[['Latitude', 'Longitude']]
locations_mid = log_song_data_unique.loc[log_song_data_unique['Region'].isin(['mid'])].copy().reset_index(drop=True)[
                ['Latitude', 'Longitude']]

col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear',
               'RecordingTime',
               'Latitude', 'Longitude']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# get mid data separately
data_mid = data_subset.loc[data_subset['Region'].isin(['mid'])].copy().reset_index(drop=True)

# use only east and west data
data = data_subset.drop(data_subset.loc[data_subset['Region'].isin(['mid', 'south'])].index).copy().reset_index(
    drop=True)

'''
set up labels --> the categories we want to be able to sort the data into and their actual category
'''
label_names = data.Region.unique()
labels = pd.get_dummies(data.Region, drop_first=True).values.ravel()

'''
all 16 song variables
'''
# # organizing data into sets
# feature_names = data.columns[1:].values
# features = data.loc[:, data.columns != 'Region'].values
#
# train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=42)
#
# # initialize our classifier
# gnb = GaussianNB()
#
# # train our classifier
# model = gnb.fit(train, train_labels)
#
# # make predictions
# preds = gnb.predict(test)
#
# # evaluate accuracy
# prediction = {'all 16 variables': accuracy_score(test_labels, preds)}
# print(accuracy_score(test_labels, preds))
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/MachineLearningClassifier'
#           '/allVariablesTogether.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in sorted(prediction.items(), key=lambda kv: kv[1], reverse=True):
#        writer.writerow([key, value])


'''
all individual variables
'''
# # organizing data into sets
# predictions = dict()
# for i in data.columns[1:].values:
#
#     feature_name = i
#     feature = data.loc[:, data.columns == i].values
#
#     train, test, train_labels, test_labels = train_test_split(feature, labels, test_size=0.33, random_state=42)
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
#     predictions[feature_name] = accuracy_score(test_labels, preds)
#     # print(feature_name, accuracy_score(test_labels, preds))
# print(sorted(predictions.items(), key=lambda kv: kv[1], reverse=True))
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/MachineLearningClassifier'
#           '/allIndividuals.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
#        writer.writerow([key, value])

'''
all combinations of 2 of the 16 song variables
'''
# # organizing data into sets
# predictions = dict()
# combinations = list(itertools.combinations(data.columns[1:].values, 2))
# for i in combinations:
#
#     two_feature_names = np.asarray(i)
#     two_features = data.loc[:, two_feature_names].values
#
#     train, test, train_labels, test_labels = train_test_split(two_features, labels, test_size=0.33, random_state=42)
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
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/MachineLearningClassifier'
#           '/combosOfTwo.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
#        writer.writerow([key, value])

'''
all combinations of 3 of the 16 song variables
'''
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
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/MachineLearningClassifier'
#           '/combosOfThree.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in sorted(predictions.items(), key=lambda kv: kv[1], reverse=True):
#        writer.writerow([key, value])

"""
Use best classifier for classifying the mid region
"""
# choose features to train the dataset
three_feature_names = ['AvgNoteDuration_ms', 'AvgSilenceDuration_ms', 'AvgSyllsUpperFreq_Hz']
three_features = data.loc[:, three_feature_names].values

# organizing data into sets
train, test, train_labels, test_labels = train_test_split(three_features, labels, test_size=0.33, random_state=42)

#shuffle the lat/long of the east/west files the same way as the train_test_split does
lat_shuffle = shuffle(np.asarray(locations_eastwest['Latitude']), random_state=42)
long_shuffle = shuffle(np.asarray(locations_eastwest['Longitude']), random_state=42)

print('len of test', len(test))
print('len of train', len(train))

#get the lat/long of the test and train set
lat_test = lat_shuffle[0:len(test)]
long_test = long_shuffle[0:len(test)]

# initialize our classifier
gnb = GaussianNB()

# train our classifier
model = gnb.fit(train, train_labels)

# make predictions on east/west as well as on the mid
preds = gnb.predict(test)
preds_mid = gnb.predict(data_mid.loc[:, three_feature_names].values)

# geographic plot of predictions

# Set the dimension of the figure
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi, frameon=False)

#make the geographic background map
m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
m.drawcoastlines(color='k', linewidth=1.5)
m.drawcountries(color='k', linewidth=1.5)
m.drawstates(color='gray')
m.drawmapboundary(fill_color='w', color='none')

# set east and west colors based on prediction
preds_colors = preds.tolist()
for i, item in enumerate(preds_colors):
    if item == 0:
        preds_colors[i] = '#1f78b4'
    if item == 1:
        preds_colors[i] = '#33a02c'

preds_mid_colors = preds_mid.tolist()
for i, item in enumerate(preds_mid_colors):
    if item == 0:
        preds_mid_colors[i] = '#1f78b4'
    if item == 1:
        preds_mid_colors[i] = '#33a02c'

#plot points at sampling locations
m.scatter(long_test, lat_test, latlon=True,
          s=100, label=None, zorder=10, c=tuple(preds_colors), edgecolor='black', linewidth=1)

#plot points at sampling locations
m.scatter(locations_mid['Longitude'], locations_mid['Latitude'], latlon=True,
          s=100, label=None, zorder=10, c=tuple(preds_mid_colors), edgecolor='black', linewidth=1)

# m.hexbin(data_downsampled['Longitude'], data_downsampled['Latitude'], bins='log', mincnt=1, gridsize=50, cmap='cool')
# cb = m.colorbar()
#
# ticks_number = []
# t_old = []
# for t in cb.ax.get_yticklabels():
#     t_old.append(float(t.get_text()))
#     new_tick = float(t.get_text().replace(t.get_text(), str(10**float(t.get_text()))))
#     ticks_number.append(new_tick)
# cb.set_ticks(t_old)
# cb.set_ticklabels(["%.2f" % e for e in ticks_number])
# cb.ax.tick_params(labelsize=25)
# cb.set_label('Number', size=25)
#
# plt.tight_layout()
#
# #create a legend
# for a in [1, 5, 20, 40]:
#     plt.scatter([], [], c='k', s=100*a, label=str(a), edgecolors='k', linewidths=1)
# plt.legend(scatterpoints=1, frameon=False, labelspacing=0.5, columnspacing=1,
#            loc='lower right', fontsize=50)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject/StatsOfFinalData_withReChipperReExported/MachineLearningClassifier/" +
               'BestPrediction_geoPlot' + '.pdf')

pdf.savefig(dpi=fig.dpi, orientation='landscape')
pdf.close()

plt.show()

# evaluate accuracy
prediction = accuracy_score(test_labels, preds)
print(prediction)
