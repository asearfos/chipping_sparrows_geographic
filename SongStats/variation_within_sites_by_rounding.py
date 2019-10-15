import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
from scipy.stats import ranksums, levene
import csv
from matplotlib.ticker import FuncFormatter

"""
Load data song data
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear',
               'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)
print(data_subset.shape)

# use only east, west and south data for wilcoxon rank sums
data_for_wrs = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)

# round latitude and longitude to ~1km
data_for_wrs_rounded = data_for_wrs.round({'Latitude': 2, 'Longitude': 2})

# add another column with e,w,s and heavily sampled sites
data_for_wrs_rounded['Site'] = data_for_wrs_rounded['Region']

print(data_for_wrs_rounded.shape)
print(data_for_wrs_rounded.duplicated(subset=('Latitude', 'Longitude')).sum())
with pd.option_context('display.max_rows', None):
    print(data_for_wrs_rounded.groupby(['Latitude', 'Longitude'],
                                       as_index=False).size().sort_values(
        ascending=False))

def add_site(x):

    if x['Latitude'] == 42.37 and x['Longitude'] == -72.52:
        return 'Amherst MA'
    elif x['Latitude'] == 40.08 and x['Longitude'] == -82.92:
        return 'N Columbus OH'
    elif x['Latitude'] == 39.96 and x['Longitude'] == -83.00:
        return 'Columbus OH'
    elif x['Latitude'] == 42.28 and x['Longitude'] == -72.31:
        return 'Ware MA'
    elif x['Latitude'] == 40.42 and x['Longitude'] == -82.91:
        return 'Ashley OH'
    else:
        return x['Site']


data_for_wrs_rounded['Site'] = data_for_wrs_rounded.apply(add_site, axis=1)


print(data_for_wrs_rounded['Site'].value_counts())

"""
Brown-Forsythe test (Levene's with median)
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/'
          'StatsOfFinalData_withReChipperReExported/AnimalBehaviourRevisions'
          '/BoxPlots_Norm_bySite/database_BrownForsythe_variances.csv',
          'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'E-Col p-value',
                         'E-NCol p-value',
                         'E-Ash p-value',
                         'E-Am p-value',
                         'E-Ware p-value',
                         'E variance',
                         'Col variance',
                         'NCol variance',
                         'Ash variance',
                         'Am variance',
                         'Ware variance'
                         ])

    for sv in data_for_wrs.columns[4:-1]:
        e = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                     'east', sv]
        Col = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                       'Columbus OH', sv]
        NCol = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                        'N Columbus OH', sv]
        Ash = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                       'Ashley OH', sv]
        Am = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                      'Amherst MA', sv]
        Ware = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                        'Ware MA', sv]

        filewriter.writerow([sv,
                             levene(e, Col, center='median')[1],
                             levene(e, NCol, center='median')[1],
                             levene(e, Ash, center='median')[1],
                             levene(e, Am, center='median')[1],
                             levene(e, Ware, center='median')[1],
                             np.var(e),
                             np.var(Col),
                             np.var(NCol),
                             np.var(Ash),
                             np.var(Am),
                             np.var(Ware)
                             ])


"""
Discrete Stats Tests using databases:
Wilcoxon Rank sums for databasess: BL, EB, ML, WC, XC and the 16 song 
variables
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/'
          'StatsOfFinalData_withReChipperReExported/AnimalBehaviourRevisions'
          '/BoxPlots_Norm_bySite/database_WilcoxonRanksums.csv', 'wb') as \
        file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'E-Col Wilcoxon p', 'E-Col p-value',
                         'E-NCol Wilcoxon p', 'E-NCol p-value',
                         'E-Ash Wilcoxon p', 'E-Ash p-value',
                         'E-Am Wilcoxon p', 'E-Am p-value',
                         'E-Ware Wilcoxon p', 'E-Ware p-value'
                         ])

    for sv in data_for_wrs_rounded.columns[4:-1]:
        e = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                     'east', sv]
        Col = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                       'Columbus OH', sv]
        NCol = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                        'N Columbus OH', sv]
        Ash = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                       'Ashley OH', sv]
        Am = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                      'Amherst MA', sv]
        Ware = data_for_wrs_rounded.loc[data_for_wrs_rounded['Site'] ==
                                        'Ware MA', sv]

        filewriter.writerow([sv,
                             ranksums(e, Col)[0], ranksums(e, Col)[1],
                             ranksums(e, NCol)[0], ranksums(e, NCol)[1],
                             ranksums(e, Ash)[0], ranksums(e, Ash)[1],
                             ranksums(e, Am)[0], ranksums(e, Am)[1],
                             ranksums(e, Ware)[0], ranksums(e, Ware)[1]
                             ])

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

log_var = {4: 'ms', 8: 'ms', 9: 'ms', 15: 'number', 17: 'number', 18: 'ms'}
log_convert_var = {10: 'kHz', 5: 'kHz', 6: 'kHz', 7: 'kHz', 11: 'kHz',
                   12: 'kHz', 13: 'seconds'}
log_convert_inverse_var = {16: 'number/second'}
no_log = {14: '%'}
no_log_convert = {19: 'kHz'}
print(data_for_wrs_rounded.columns)

# take e^x for y-axis
for key, value in log_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    ax = sns.boxplot(x='Site',
                     y=data_for_wrs_rounded.columns[key],
                     data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2,
                     order=['south', 'west', 'east', 'Columbus OH',
                            'N Columbus OH', 'Ashley OH', 'Amherst MA',
                            'Ware MA'])
    ax = sns.stripplot(x='Site',
                       y=data_for_wrs_rounded.columns[key],
                       data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6,
                       order=['south', 'west', 'east', 'Columbus OH',
                              'N Columbus OH', 'Ashley OH', 'Amherst MA',
                              'Ware MA'],
                       palette=['#f17300', '#33a02c', '#1f78b4',
                                'grey', 'grey', 'grey', 'grey', 'grey'])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-4] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    # plt.xticks(rotation='vertical')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported\AnimalBehaviourRevisions"
                "\BoxPlots_Norm_bySite/" + data_for_wrs_rounded.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    # plt.close()

    # plt.show()

# take e^x for each variable and also convert from Hz to kHz or ms to seconds
for key, value in log_convert_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    ax = sns.boxplot(x='Site',
                     y=data_for_wrs_rounded.columns[key],
                     data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2,
                     order=['south', 'west', 'east', 'Columbus OH',
                            'N Columbus OH', 'Ashley OH', 'Amherst MA',
                            'Ware MA'])
    ax = sns.stripplot(x='Site',
                       y=data_for_wrs_rounded.columns[key],
                       data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6,
                       order=['south', 'west', 'east', 'Columbus OH',
                              'N Columbus OH', 'Ashley OH', 'Amherst MA',
                              'Ware MA'],
                       palette=['#f17300', '#33a02c', '#1f78b4',
                                'grey', 'grey', 'grey', 'grey', 'grey'])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-4] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported\AnimalBehaviourRevisions"
                "\BoxPlots_Norm_bySite/" + data_for_wrs_rounded.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='Site',
                     y=data_for_wrs_rounded.columns[key],
                     data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2,
                     order=['south', 'west', 'east', 'Columbus OH',
                            'N Columbus OH', 'Ashley OH', 'Amherst MA',
                            'Ware MA'])
    ax = sns.stripplot(x='Site',
                       y=data_for_wrs_rounded.columns[key],
                       data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6,
                       order=['south', 'west', 'east', 'Columbus OH',
                              'N Columbus OH', 'Ashley OH', 'Amherst MA',
                              'Ware MA'],
                       palette=['#f17300', '#33a02c', '#1f78b4',
                                'grey', 'grey', 'grey', 'grey', 'grey'])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-4] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)*1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported\AnimalBehaviourRevisions"
                "\BoxPlots_Norm_bySite/" + data_for_wrs_rounded.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='Site',
                     y=data_for_wrs_rounded.columns[key],
                     data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2,
                     order=['south', 'west', 'east', 'Columbus OH',
                            'N Columbus OH', 'Ashley OH', 'Amherst MA',
                            'Ware MA'])
    ax = sns.stripplot(x='Site',
                       y=data_for_wrs_rounded.columns[key],
                       data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6,
                       order=['south', 'west', 'east', 'Columbus OH',
                              'N Columbus OH', 'Ashley OH', 'Amherst MA',
                              'Ware MA'],
                       palette=['#f17300', '#33a02c', '#1f78b4',
                                'grey', 'grey', 'grey', 'grey', 'grey'])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-4] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % x))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported\AnimalBehaviourRevisions"
                "\BoxPlots_Norm_bySite/" + data_for_wrs_rounded.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='Site',
                     y=data_for_wrs_rounded.columns[key],
                     data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                     color='None',
                     fliersize=0,
                     width=0.5,
                     linewidth=2,
                     order=['south', 'west', 'east', 'Columbus OH',
                            'N Columbus OH', 'Ashley OH', 'Amherst MA',
                            'Ware MA'])
    ax = sns.stripplot(x='Site',
                       y=data_for_wrs_rounded.columns[key],
                       data=data_for_wrs_rounded[['Site', data_for_wrs_rounded.columns[key]]],
                       size=7,
                       jitter=True,
                       lw=1,
                       alpha=0.6,
                       order=['south', 'west', 'east', 'Columbus OH',
                              'N Columbus OH', 'Ashley OH', 'Amherst MA',
                              'Ware MA'],
                       palette=['#f17300', '#33a02c', '#1f78b4',
                                'grey', 'grey', 'grey', 'grey', 'grey'])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-4] + ' (' + value + ')', fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (x/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported\AnimalBehaviourRevisions"
                "\BoxPlots_Norm_bySite/" + data_for_wrs_rounded.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()