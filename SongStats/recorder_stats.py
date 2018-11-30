import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
import csv
from mpl_toolkits.basemap import Basemap
from scipy.stats import ranksums
from matplotlib.ticker import FuncFormatter


"""
Load song and recorder type data, organize/subset for testing differences in recorder type
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis and any missing data
col_to_skip = ['FromDatabase', 'ComparedStatus', 'RecordingDay']
data_for_song = log_song_data_unique.drop(col_to_skip, axis=1)
fn = lambda x: x['CatalogNo'].split('.')[0]
data_for_song['CatalogNo'] = data_for_song.apply(fn, axis=1).astype(str)
data_for_song['RecordingTime'] = pd.to_datetime(data_for_song['RecordingTime'])
data_for_song['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_song['RecordingTime']]

# load recorder data
recorder_path = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject/recorder spreadsheets from nicole/" \
                "recorderData_MLeBirdBorror_noUnspecified.csv"
data_for_rec = pd.DataFrame.from_csv(recorder_path, header=0, index_col=None)
data_for_rec['catalogNumber'] = data_for_rec['catalogNumber'].astype(str)

# combine tables using CatalogNo
combined_table = data_for_song.merge(data_for_rec, how='left', left_on='CatalogNo', right_on='catalogNumber')
print(combined_table.shape)

# fill na with unknown for recorder_class
combined_table.recorder_class.fillna('Unknown', inplace=True)
combined_table.to_csv("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/"
                      "RecorderAnalysis/PaperVersion/combinedSongRecTable.csv")

#checking the number of each category
print(combined_table[combined_table['recorder_class'] == 'Analog'].shape)
print(combined_table[combined_table['recorder_class'] == 'Digital'].shape)
print(combined_table[combined_table['recorder_class'] == 'Phone'].shape)
print(combined_table[combined_table['recorder_class'] == 'Other'].shape)
print(combined_table[combined_table['recorder_class'] == 'Unknown'].shape)


""""
Wilcoxon Ranksums
"""
metadata = ['Latitude', 'Longitude', 'RecordingYear', 'RecordingMonth', 'RecordingTime']

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/RecorderAnalysis/PaperVersion/recorderMetaData_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Fixed Variable',
                         'Analog vs Digital p-value',
                         'Analog vs Phone p-value',
                         'Digital vs Phone p-value'])
    for sv in metadata:
        a = combined_table.loc[combined_table['recorder_class'] == 'Analog', sv]
        d = combined_table.loc[combined_table['recorder_class'] == 'Digital', sv]
        p = combined_table.loc[combined_table['recorder_class'] == 'Phone', sv]
        filewriter.writerow([sv,
                             ranksums(a, d)[1],
                             ranksums(a, p)[1],
                             ranksums(d, p)[1]])


"""
Box Plots for recorder type and metadata
"""
for sv in metadata:
    fig = plt.figure(figsize=(7, 11))
    sns.set(style='white')
    ax = sns.boxplot(x='recorder_class', y=sv, data=combined_table[['recorder_class', sv]], color='None',
                     fliersize=0, width=0.5, linewidth=2,  order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=sv, data=combined_table[['recorder_class', sv]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'], size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(sv, fontsize=30)
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
                "/RecorderAnalysis/PaperVersion/" + sv + 'RecorderSignalType_AnalogDigital' + '.pdf', type='pdf',
                dpi=fig.dpi,
                bbox_inches='tight',
                transparent=True)
    # plt.show()

""""
Wilcoxon Ranksums
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/RecorderAnalysis/PaperVersion/recorderSongVar_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'Analog vs Digital p-value',
                         'Analog vs Phone p-value',
                         'Digital vs Phone p-value'])

    for sv in combined_table.columns[7:23]:
        a = combined_table.loc[combined_table['recorder_class'] == 'Analog', sv]
        d = combined_table.loc[combined_table['recorder_class'] == 'Digital', sv]
        p = combined_table.loc[combined_table['recorder_class'] == 'Phone', sv]
        filewriter.writerow([sv,
                             ranksums(a, d)[1],
                             ranksums(a, p)[1],
                             ranksums(d, p)[1]])


""""
Box plot of 16 song features for recorder type
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

log_var = {7: 'ms', 11: 'ms', 12: 'ms', 18: 'number', 20: 'number', 21: 'ms'}
log_convert_var = {8: 'kHz', 9: 'kHz', 10: 'kHz', 13: 'kHz', 14: 'kHz', 15: 'kHz', 16: 'seconds'}
log_convert_inverse_var = {19: 'number/second'}
no_log = {17: '%'}
no_log_convert = {22: 'kHz'}

# take e^x for y-axis
for key, value in log_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white')
    ax = sns.boxplot(x='recorder_class', y=combined_table.columns[key],
                     data=combined_table[['recorder_class', combined_table.columns[key]]], color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=combined_table.columns[key],
                       data=combined_table[['recorder_class', combined_table.columns[key]]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], combined_table.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/RecorderAnalysis"
                "/PaperVersion/" + combined_table.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='recorder_class', y=combined_table.columns[key],
                     data=combined_table[['recorder_class', combined_table.columns[key]]], color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=combined_table.columns[key],
                       data=combined_table[['recorder_class', combined_table.columns[key]]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], combined_table.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/RecorderAnalysis"
                "/PaperVersion/" + combined_table.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='recorder_class', y=combined_table.columns[key],
                     data=combined_table[['recorder_class', combined_table.columns[key]]], color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=combined_table.columns[key],
                       data=combined_table[['recorder_class', combined_table.columns[key]]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], combined_table.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)*1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/RecorderAnalysis"
                "/PaperVersion/" + combined_table.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='recorder_class', y=combined_table.columns[key],
                     data=combined_table[['recorder_class', combined_table.columns[key]]], color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=combined_table.columns[key],
                       data=combined_table[['recorder_class', combined_table.columns[key]]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], combined_table.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % x))


    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/RecorderAnalysis"
                "/PaperVersion/" + combined_table.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x='recorder_class', y=combined_table.columns[key],
                     data=combined_table[['recorder_class', combined_table.columns[key]]], color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'])
    ax = sns.stripplot(x='recorder_class', y=combined_table.columns[key],
                       data=combined_table[['recorder_class', combined_table.columns[key]]],
                       order=['Analog', 'Digital', 'Phone', 'Other', 'Unknown'],
                       palette=['black', 'grey', 'white', 'red', 'pink'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], combined_table.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (x/1000)))


    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/RecorderAnalysis"
                "/PaperVersion/" + combined_table.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()

