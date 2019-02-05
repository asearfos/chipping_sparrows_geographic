import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
import csv
from scipy.stats import ranksums
from matplotlib.ticker import FuncFormatter


"""
Load data and organize/subset for testing changes over years
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
data_for_year = log_song_data_unique.drop(col_to_skip, axis=1)
data_for_year['RecordingTime'] = pd.to_datetime(data_for_year['RecordingTime'])
data_for_year['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_year['RecordingTime']]
print(data_for_year)
data_for_year = data_for_year.dropna(subset=['RecordingYear'])
print(data_for_year)

#divide up by year
before_1984 = data_for_year[data_for_year.RecordingYear < 1984]
after_1984 = data_for_year[data_for_year.RecordingYear >= 1984]

print(before_1984.loc[before_1984['Region'].isin(['east'])].shape)
print(before_1984.loc[before_1984['Region'].isin(['west'])].shape)
print(after_1984.loc[after_1984['Region'].isin(['east'])].shape)
print(after_1984.loc[after_1984['Region'].isin(['west'])].shape)

before_1959 = data_for_year[data_for_year.RecordingYear < 1959]
after_1959 = data_for_year[data_for_year.RecordingYear >= 1959]

# """
# Histogram plot of the number of recordings per year
# """
# sns.distplot(data_for_year['RecordingYear'], bins=69)
# plt.show()
#

"""
See if there is a difference in spread of year of recording between East and West
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/YearRegion'
          '/yearRegion_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'EW Wilcoxon p', 'EW p-value'])

    e = data_for_year.loc[data_for_year['Region'] == 'east', 'RecordingYear']
    w = data_for_year.loc[data_for_year['Region'] == 'west', 'RecordingYear']

    filewriter.writerow(['RecordingYear', ranksums(e, w)[0], ranksums(e, w)[1]])

""""
Box plot of results
"""

data_for_year = data_for_year.drop(data_for_year[data_for_year.Region == 'mid'].index).copy().reset_index(drop=True)
data_for_year = data_for_year.drop(data_for_year[data_for_year.Region == 'south'].index).copy().reset_index(drop=True)

fig = plt.figure(figsize=(7, 11))
my_dpi = 96
sns.set(style='white',
        rc={"font.style": "normal",
            'lines.markersize': 2,
            'axes.labelsize': 20,
            'xtick.labelsize': 18,
            'ytick.labelsize': 18,
            })

ax = sns.boxplot(x='Region', y='RecordingYear',
                 data=data_for_year, order=['east', 'west'],
                 color='None',
                 fliersize=0, width=0.5,
                 linewidth=2)
ax = sns.stripplot(x='Region', y='RecordingYear',
                   data=data_for_year, order=['east', 'west'],
                   palette=['#1f78b4', '#33a02c'],
                   size=7, jitter=True, lw=1, alpha=0.6)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

plt.setp(ax.spines.values(), linewidth=2)

plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
            "/YearRegion/yearRegionBoxPlot.pdf", type='pdf', dpi=fig.dpi,
            bbox_inches='tight', transparent=True)
# plt.cla()
# plt.clf()
plt.close()

plt.show()
quit()
""""
Wilcoxon Ranksums (all regions and for east and west separately --> Print out results to csv)
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/YearAnalysis/PaperVersion/year_WilcoxonRanksums'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'All Regions w', 'All Regions p-value', 'East w', 'East p-value', 'West w',
                         'West p-value'])
    for sv in data_for_year.columns[7:]:
        b = np.asarray(before_1984[sv])
        a = np.asarray(after_1984[sv])
        b_e = np.asarray(before_1984.loc[before_1984['Region'] == 'east', sv])
        a_e = np.asarray(after_1984.loc[after_1984['Region'] == 'east', sv])
        b_w = np.asarray(before_1984.loc[before_1984['Region'] == 'west', sv])
        a_w = np.asarray(after_1984.loc[after_1984['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b, a)[0], ranksums(b, a)[1], ranksums(b_e, a_e)[0], ranksums(b_e, a_e)[1],
                            ranksums(b_w, a_w)[0], ranksums(b_w, a_w)[1]])

"""
Wilcoxon ranksums --> split into before and after 1984 and see if there is a difference in east and west within one
of those categories
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/YearAnalysis'
          '/PaperVersion/year_WilcoxonRanksums_regionDiffsWithinTimeframe'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'Before 1984 w', 'Before 1984 p-value',
                         'After 1984 w', 'After 1984  p-value'])
    for sv in data_for_year.columns[7:]:
        b = np.asarray(before_1984[sv])
        a = np.asarray(after_1984[sv])
        b_e = np.asarray(before_1984.loc[before_1984['Region'] == 'east', sv])
        a_e = np.asarray(after_1984.loc[after_1984['Region'] == 'east', sv])
        b_w = np.asarray(before_1984.loc[before_1984['Region'] == 'west', sv])
        a_w = np.asarray(after_1984.loc[after_1984['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b_e, b_w)[0], ranksums(b_e, b_w)[1],
                             ranksums(a_e, a_w)[0], ranksums(a_e, a_w)[1]])


""""
Box plot of song results for year
"""
yr = '1984'
data_for_year[yr] = np.where(data_for_year['RecordingYear'] < 1984, 'before', 'after')
print(data_for_year.columns)
print(data_for_year.shape)

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
    ax = sns.boxplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                     color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['before', 'after'])
    ax = sns.stripplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                       order=['before', 'after'],
                       palette=['black', 'grey'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], data_for_year.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/YearAnalysis"
                "/PaperVersion/" + data_for_year.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                     color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['before', 'after'])
    ax = sns.stripplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                       order=['before', 'after'],
                       palette=['black', 'grey'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], data_for_year.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/YearAnalysis"
                "/PaperVersion/" + data_for_year.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                     color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['before', 'after'])
    ax = sns.stripplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                       order=['before', 'after'],
                       palette=['black', 'grey'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], data_for_year.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)*1000)))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/YearAnalysis"
                "/PaperVersion/" + data_for_year.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                     color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['before', 'after'])
    ax = sns.stripplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                       order=['before', 'after'],
                       palette=['black', 'grey'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], data_for_year.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % x))


    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/YearAnalysis"
                "/PaperVersion/" + data_for_year.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
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
    ax = sns.boxplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                     color='None',
                     fliersize=0, width=0.5,
                     linewidth=2, order=['before', 'after'])
    ax = sns.stripplot(x=yr, y=data_for_year.columns[key], data=data_for_year[[yr, data_for_year.columns[key]]],
                       order=['before', 'after'],
                       palette=['black', 'grey'],
                       size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-7] + ' (' + value + ')', fontsize=30)
    print(song_variables[key-7], data_for_year.columns[key])
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (x/1000)))


    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/YearAnalysis"
                "/PaperVersion/" + data_for_year.columns[key] + '_noLogAxis_largerFont' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()


