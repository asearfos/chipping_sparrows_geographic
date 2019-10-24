import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
from scipy.stats import ranksums
import csv
from matplotlib.ticker import FuncFormatter

"""
Load data song data
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data[
    'ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(drop=True)
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay',
               'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)
# print(data_subset.shape)
# print(data_subset.Region.value_counts())

# use only east, west and south data for wilcoxon rank sums
data_for_wrs = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)
data_for_wrs_rounded = data_for_wrs.round({'Latitude': 2, 'Longitude': 2})
# print(data_for_wrs.shape)

col_to_skip_notYear = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingTime']
data_subset_wYear = log_song_data_unique.drop(col_to_skip_notYear, axis=1)
data_subset_wYear = data_subset_wYear.dropna(subset=['RecordingYear'])
data_subset_wYear = data_subset_wYear.drop(data_subset_wYear[data_subset_wYear.Region == 'mid'].index).copy().reset_index(drop=True)
data_subset_wYear_rounded = data_subset_wYear.round({'Latitude': 2, 'Longitude': 2})


"""
Discrete Stats Tests using Regions:
Wilcoxon Rank sums for regions: east, west, south and the 16 song variables
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported/AnimalBehaviourRevisions'
          '/BoxPlots_Norm/region_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'EW Wilcoxon p', 'EW p-value',
                         'ES Wilcoxon p', 'ES p-value',
                         'WS Wilcoxon p', 'WS p-value'])

    for sv in data_for_wrs.columns[3:]:
        e = data_for_wrs.loc[data_for_wrs['Region'] == 'east', sv]
        w = data_for_wrs.loc[data_for_wrs['Region'] == 'west', sv]
        s = data_for_wrs.loc[data_for_wrs['Region'] == 'south', sv]

        filewriter.writerow([sv,
                             ranksums(e, w)[0], ranksums(e, w)[1],
                             ranksums(e, s)[0], ranksums(e, s)[1],
                             ranksums(w, s)[0], ranksums(w, s)[1]])

""""
Box plot of results
"""
song_variables = ['Mean Note Duration',
                  'Mean Note Frequency Modulation',
                  'Mean Note Frequency Trough',
                  'Mean Note Frequency Peak',
                  'Mean Inter-Syllable Silence Duration',
                  'Mean Syllable Duration',
                  'Mean Syllable Frequency Modulation',
                  'Mean Syllable Frequency Trough',
                  'Mean Syllable Frequency Peak',
                  'Duration of Song Bout',
                  'Mean Stereotypy of Repeated Syllables',
                  'Number of Notes per Syllable',
                  'Syllable Rate',
                  'Total Number of Syllables',
                  'Standard Deviation of Note Duration',
                  'Standard Deviation of Note Frequency Modulation']

log_var = {3: 'ms', 7: 'ms', 8: 'ms', 14: 'number', 16: 'number', 17: 'ms'}
log_convert_var = {9: 'kHz', 4: 'kHz', 5: 'kHz', 6: 'kHz', 10: 'kHz', 11: 'kHz', 12: 'seconds'}
log_convert_inverse_var = {15: 'number/second'}
no_log = {13: '%'}
no_log_convert = {18: 'kHz'}
print(data_for_wrs.columns)

# take e^x for y-axis
for key, value in log_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    sns.set_style('ticks')
    ax = sns.boxplot(x='Region',
                     y=data_for_wrs.columns[key],
                     data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                     order=['south', 'west', 'east'],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2)
    ax = sns.stripplot(x='Region',
                       y=data_for_wrs.columns[key],
                       data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                       order=['south', 'west', 'east'],
                       palette=['#f17300', '#33a02c', '#1f78b4'],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "/AnimalBehaviourRevisions/BoxPlots_Norm"
                "/PaperVersion_noLogAxis_largerFont/" + data_for_wrs.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

# take e^x for each variable and also convert from Hz to kHz or ms to seconds
for key, value in log_convert_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    sns.set_style('ticks')
    ax = sns.boxplot(x='Region',
                     y=data_for_wrs.columns[key],
                     data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                     order=['south', 'west', 'east'],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2)
    ax = sns.stripplot(x='Region', y=data_for_wrs.columns[key],
                       data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                       order=['south', 'west', 'east'],
                       palette=['#f17300', '#33a02c', '#1f78b4'],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "/AnimalBehaviourRevisions/BoxPlots_Norm"
                "/PaperVersion_noLogAxis_largerFont/" + data_for_wrs.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

# take e^x for each variable and convert from 1/ms to 1/seconds
for key, value in log_convert_inverse_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    sns.set_style('ticks')
    ax = sns.boxplot(x='Region',
                     y=data_for_wrs.columns[key],
                     data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                     order=['south', 'west', 'east'],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2)
    ax = sns.stripplot(x='Region',
                       y=data_for_wrs.columns[key],
                       data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                       order=['south', 'west', 'east'],
                       palette=['#f17300', '#33a02c', '#1f78b4'],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)*1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "/AnimalBehaviourRevisions/BoxPlots_Norm"
                "/PaperVersion_noLogAxis_largerFont/" + data_for_wrs.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

# are not log(value) so no need to take exponential and no conversion
for key, value in no_log.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    sns.set_style('ticks')
    ax = sns.boxplot(x='Region',
                     y=data_for_wrs.columns[key],
                     data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                     order=['south', 'west', 'east'],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2)
    ax = sns.stripplot(x='Region',
                       y=data_for_wrs.columns[key],
                       data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                       order=['south', 'west', 'east'],
                       palette=['#f17300', '#33a02c', '#1f78b4'],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % x))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "/AnimalBehaviourRevisions/BoxPlots_Norm"
                "/PaperVersion_noLogAxis_largerFont/" + data_for_wrs.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

# are not log(value) so no need to take exponential, convert from Hz to kHz
for key, value in no_log_convert.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    sns.set_style('ticks')
    ax = sns.boxplot(x='Region',
                     y=data_for_wrs.columns[key],
                     data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                     order=['south', 'west', 'east'],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2)
    ax = sns.stripplot(x='Region',
                       y=data_for_wrs.columns[key],
                       data=data_for_wrs[['Region', data_for_wrs.columns[key]]],
                       order=['south', 'west', 'east'],
                       palette=['#f17300', '#33a02c', '#1f78b4'],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (x/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "/AnimalBehaviourRevisions/BoxPlots_Norm"
                "/PaperVersion_noLogAxis_largerFont/" + data_for_wrs.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

"""
Downsampling of data to check we get the same results - only one random
sample from each lat/long
"""

# load in list of random seeds
seed_list = np.genfromtxt('C:/Users/abiga\Box '
                          'Sync\Abigail_Nicole\ChippiesProject'
                          '\FinalDataCompilation\RandomSeeds.csv',
                          delimiter=',', dtype='int')

ranksums_EW = pd.DataFrame(index=range(1000),
                           columns=[data_for_wrs_rounded.columns[3:]])
ranksums_ES = pd.DataFrame(index=range(1000),
                           columns=[data_for_wrs_rounded.columns[3:]])
ranksums_WS = pd.DataFrame(index=range(1000),
                           columns=[data_for_wrs_rounded.columns[3:]])

for r, seed in zip(range(1000), seed_list):
    sample = data_for_wrs_rounded.groupby(['Latitude', 'Longitude']).apply(
        lambda x: x.sample(1, random_state=seed)).reset_index(drop=True)

    for sv in sample.columns[3:]:
        e = sample.loc[sample['Region'] == 'east', sv]
        w = sample.loc[sample['Region'] == 'west', sv]
        s = sample.loc[sample['Region'] == 'south', sv]

        ranksums_EW.iloc[r][sv] = ranksums(e, w)[1]
        ranksums_ES.iloc[r][sv] = ranksums(e, s)[1]
        ranksums_WS.iloc[r][sv] = ranksums(w, s)[1]

downsampling_results = pd.concat([ranksums_EW.max(axis=0),
                                  ranksums_EW.min(axis=0),
                                  ranksums_ES.max(axis=0),
                                  ranksums_ES.min(axis=0),
                                  ranksums_WS.max(axis=0),
                                  ranksums_WS.min(axis=0)],
                                 axis=1,
                                 keys=['EW_max', 'EW_min',
                                       'ES_max', 'ES_min',
                                       'WS_max', 'WS_min'])
downsampling_results.to_csv('C:/Users/abiga/Box '
                            'Sync/Abigail_Nicole/ChippiesProject'
                            '/StatsOfFinalData_withReChipperReExported'
                            '/AnimalBehaviourRevisions/BoxPlots_Norm'
                            '/region_WilcoxonRanksums_downsampled.csv')


"""
See if there is a difference in spread of year of 
recording between East and West (BEFORE downsampling)
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions/YearRegion'
          '/yearRegion_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'EW Wilcoxon p', 'EW p-value'])

    e = data_subset_wYear.loc[data_subset_wYear['Region'] == 'east',
                              'RecordingYear']
    w = data_subset_wYear.loc[data_subset_wYear['Region'] == 'west',
                              'RecordingYear']

    filewriter.writerow(['RecordingYear',
                         ranksums(e, w)[0],
                         ranksums(e, w)[1]])


"""
See if there is a difference in spread of year of 
recording between East and West (after downsampling)
"""

ranksums_year = pd.DataFrame(index=range(1000),
                             columns=['RecordingYear pvalue'])

for r, seed in zip(range(1000), seed_list):
    sample = data_subset_wYear_rounded.groupby(['Latitude', 'Longitude']).apply(
        lambda x: x.sample(1, random_state=seed)).reset_index(drop=True)

    e_yr = sample.loc[sample['Region'] == 'east', 'RecordingYear']
    w_yr = sample.loc[sample['Region'] == 'west', 'RecordingYear']

    ranksums_year.iloc[r]['RecordingYear pvalue'] = ranksums(e_yr, w_yr)[1]

downsampling_results_yr = pd.concat([ranksums_year.max(axis=0),
                                     ranksums_year.min(axis=0)],
                                    axis=1,
                                    keys=['year_max', 'year_min'])
downsampling_results_yr.to_csv('C:/Users/abiga/Box '
                            'Sync/Abigail_Nicole/ChippiesProject'
                            '/StatsOfFinalData_withReChipperReExported'
                            '/AnimalBehaviourRevisions/YearRegion'
                            '/yearRegion_WilcoxonRanksums_downsampled.csv')

