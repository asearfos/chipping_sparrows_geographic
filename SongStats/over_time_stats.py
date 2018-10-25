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
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingTime']
data_for_year = log_song_data_unique.drop(col_to_skip, axis=1).dropna(axis=0)

#divide up by year
before_1984 = data_for_year[data_for_year.RecordingYear < 1984]
after_1984 = data_for_year[data_for_year.RecordingYear >= 1984]

before_1959 = data_for_year[data_for_year.RecordingYear < 1959]
after_1959 = data_for_year[data_for_year.RecordingYear >= 1959]

"""
Histogram plot of the number of recordings per year
"""
sns.distplot(data_for_year['RecordingYear'], bins=69)
plt.show()

"""
Location of data by year
"""

# Set the dimension of the figure
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi, frameon=False)

#make the geographic background map
m = Basemap(llcrnrlat=10, llcrnrlon=-140, urcrnrlat=65, urcrnrlon=-62)
m.drawcoastlines(color='gray')
m.drawcountries(color='k', linewidth=1)
m.drawstates(color='gray')
m.drawmapboundary(fill_color='w', color='none')

# # #plot points at sampling locations
# m.scatter(before_1984['Longitude'], before_1984['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
#           edgecolor='black', linewidth=1)
#
# #plot points at sampling locations
# m.scatter(after_1984['Longitude'], after_1984['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
#           edgecolor='black', linewidth=1)
#
# plt.tight_layout()
#
# plt.savefig("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported"
#             "/YearAnalysis/Year_spreadOfDataBeforeAndAfter1984.pdf", type='pdf', dpi=fig.dpi, bbox_inches='tight')

# plot points at sampling locations
m.scatter(before_1959['Longitude'], before_1959['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
          edgecolor='black', linewidth=1)

#plot points at sampling locations
m.scatter(after_1959['Longitude'], after_1959['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
          edgecolor='black', linewidth=1)

plt.tight_layout()

plt.savefig("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported"
            "/YearAnalysis/Year_spreadOfDataBeforeAndAfter1959.pdf", type='pdf', dpi=fig.dpi, bbox_inches='tight')

# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()

plt.show()
""""
Wilcoxon Ranksums (all regions and for east and west separately --> Print out results to csv)
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/YearAnalysis/year_WilcoxonRanksums'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'All Regions w', 'All Regions p-value', 'East w', 'East p-value', 'West w',
                         'West p-value'])
    for sv in data_for_year.columns[4:]:
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
          '/year_WilcoxonRanksums_regionDiffsWithinTimeframe'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'Before 1984 w', 'Before 1984 p-value',
                         'After 1984 w', 'After 1984  p-value'])
    for sv in data_for_year.columns[4:]:
        b = np.asarray(before_1984[sv])
        a = np.asarray(after_1984[sv])
        b_e = np.asarray(before_1984.loc[before_1984['Region'] == 'east', sv])
        a_e = np.asarray(after_1984.loc[after_1984['Region'] == 'east', sv])
        b_w = np.asarray(before_1984.loc[before_1984['Region'] == 'west', sv])
        a_w = np.asarray(after_1984.loc[after_1984['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b_e, b_w)[0], ranksums(b_e, b_w)[1],
                             ranksums(a_e, a_w)[0], ranksums(a_e, a_w)[1]])

"""
Wilcoxon ranksums --> split into before and after 1959 and see if there is a difference in east and west within one
of those categories
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/YearAnalysis'
          '/year_WilcoxonRanksums_regionDiffsWithinTimeframe_1959'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'Before 1959 w', 'Before 1959 p-value',
                         'After 1959 w', 'After 1959  p-value'])
    for sv in data_for_year.columns[4:]:
        b = np.asarray(before_1959[sv])
        a = np.asarray(after_1959[sv])
        b_e = np.asarray(before_1959.loc[before_1959['Region'] == 'east', sv])
        a_e = np.asarray(after_1959.loc[after_1959['Region'] == 'east', sv])
        b_w = np.asarray(before_1959.loc[before_1959['Region'] == 'west', sv])
        a_w = np.asarray(after_1959.loc[after_1959['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b_e, b_w)[0], ranksums(b_e, b_w)[1],
                             ranksums(a_e, a_w)[0], ranksums(a_e, a_w)[1]])


# """
# Box Plot for 'MeanSyllableStereotypy' for signal type (both years)
# """
# # not use in the paper
# data_for_year['1984'] = np.where(data_for_year['RecordingYear'] < 1984, 'before', 'after')
# data_for_year['1959'] = np.where(data_for_year['RecordingYear'] < 1959, 'before', 'after')
#
# sv = 'MeanSyllableStereotypy'
#
# for yr in ['1984', '1959']:
#     fig = plt.figure(figsize=(7, 11))
#     sns.set(style='white')
#     ax = sns.boxplot(x=yr, y=sv, data=data_for_year[[yr, sv]], color='None',
#                      fliersize=0, width=0.5, linewidth=2, order=['before', 'after'])
#     ax = sns.stripplot(x=yr, y=sv, data=data_for_year[[yr, sv]],
#                        order=['before', 'after'],
#                        palette=['gray', 'black'], size=7, jitter=True, lw=1, alpha=0.6, edgecolor=None,
#                        linewidth=0)
#
#     # Make the boxplot fully transparent
#     for patch in ax.artists:
#         r, g, b, a = patch.get_facecolor()
#         patch.set_facecolor((r, g, b, 0))
#
#     ax.set_ylabel('Mean Stereotypy of Repeated Syllables (%)', fontsize=30)
#     ax.set_xlabel('')
#     ax.tick_params(labelsize=30, direction='out')
#     ax.set(xticklabels=[])
#     plt.setp(ax.spines.values(), linewidth=2)
#
#     plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
#                 "/YearAnalysis/" + sv + 'Year_beforeVSafter_' + yr + '.pdf', type='pdf', dpi=fig.dpi,
#                 bbox_inches='tight',
#                 transparent=True)
#     # plt.show()


"""
Box Plot for 'MeanSyllableStereotypy' for signal type
"""

data_for_year['1984'] = np.where(data_for_year['RecordingYear'] < 1984, 'before', 'after')

sv = 'MeanSyllableStereotypy'
yr = '1984'

fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x=yr, y=sv, data=data_for_year[[yr, sv]], color='None',
                 fliersize=0, width=0.5, linewidth=2, order=['before', 'after'])
ax = sns.stripplot(x=yr, y=sv, data=data_for_year[[yr, sv]],
                   order=['before', 'after'],
                   palette=['black', 'grey'], size=7, jitter=True, lw=1, alpha=0.6)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

ax.set_ylabel('Mean Stereotypy of Repeated Syllables (%)', fontsize=30)
ax.set_xlabel('')
ax.tick_params(labelsize=30, direction='out')
# ax.set(xticklabels=[])
plt.setp(ax.spines.values(), linewidth=2)

plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
            "/YearAnalysis/" + sv + 'Year_beforeVSafter_' + yr + '.pdf', type='pdf', dpi=fig.dpi,
            bbox_inches='tight',
            transparent=True)
# plt.show()


"""
Box Plot for 'BoutDuration_ms' for signal type
"""

sv = 'BoutDuration_ms'
yr = '1984'

fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x=yr, y=sv, data=data_for_year[[yr, sv]], color='None',
                 fliersize=0, width=0.5, linewidth=2, order=['before', 'after'])
ax = sns.stripplot(x=yr, y=sv, data=data_for_year[[yr, sv]],
                   order=['before', 'after'],
                   palette=['black', 'grey'], size=7, jitter=True, lw=1, alpha=0.6)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

ax.set_ylabel('Duration of Song Bout (s)', fontsize=30)
ax.set_xlabel('')
ax.tick_params(labelsize=30, direction='out')
# ax.set(xticklabels=[])
plt.setp(ax.spines.values(), linewidth=2)
ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x) / 1000)))

plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
            "/YearAnalysis/" + sv + 'Year_beforeVSafter_' + yr + '.pdf', type='pdf', dpi=fig.dpi,
            bbox_inches='tight',
            transparent=True)
# plt.show()


"""
Box Plot for 'AvgNoteDuration_ms' for signal type
"""

sv = 'AvgNoteDuration_ms'
yr = '1984'

fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x=yr, y=sv, data=data_for_year[[yr, sv]], color='None',
                 fliersize=0, width=0.5, linewidth=2, order=['before', 'after'])
ax = sns.stripplot(x=yr, y=sv, data=data_for_year[[yr, sv]],
                   order=['before', 'after'],
                   palette=['black', 'grey'], size=7, jitter=True, lw=1, alpha=0.6)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

ax.set_ylabel('Mean Note Duration (ms)', fontsize=30)
ax.set_xlabel('')
ax.tick_params(labelsize=30, direction='out')
# ax.set(xticklabels=[])
plt.setp(ax.spines.values(), linewidth=2)
ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
            "/YearAnalysis/" + sv + 'Year_beforeVSafter_' + yr + '.pdf', type='pdf', dpi=fig.dpi,
            bbox_inches='tight',
            transparent=True)
# plt.show()


"""
Box Plot for 'NumSyllables' for signal type
"""

sv = 'NumSyllables'
yr = '1984'

fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x=yr, y=sv, data=data_for_year[[yr, sv]], color='None',
                 fliersize=0, width=0.5, linewidth=2, order=['before', 'after'])
ax = sns.stripplot(x=yr, y=sv, data=data_for_year[[yr, sv]],
                   order=['before', 'after'],
                   palette=['black', 'grey'], size=7, jitter=True, lw=1, alpha=0.6)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

ax.set_ylabel('Total Number of Syllables', fontsize=30)
ax.set_xlabel('')
ax.tick_params(labelsize=30, direction='out')
# ax.set(xticklabels=[])
plt.setp(ax.spines.values(), linewidth=2)
ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
            "/YearAnalysis/" + sv + 'Year_beforeVSafter_' + yr + '.pdf', type='pdf', dpi=fig.dpi,
            bbox_inches='tight',
            transparent=True)
# plt.show()