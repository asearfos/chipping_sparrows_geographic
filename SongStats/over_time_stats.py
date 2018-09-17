import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import csv
from mpl_toolkits.basemap import Basemap
from scipy.stats import ranksums

"""
Load data and organize/subset for testing changes over years
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis and any missing data
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingTime']
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

# #plot points at sampling locations
# m.scatter(before_1984['Longitude'], before_1984['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
#           edgecolor='black', linewidth=1)
#
# #plot points at sampling locations
# m.scatter(after_1984['Longitude'], after_1984['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
#           edgecolor='black', linewidth=1)

#plot points at sampling locations
m.scatter(before_1959['Longitude'], before_1959['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
          edgecolor='black', linewidth=1)

# #plot points at sampling locations
# m.scatter(after_1959['Longitude'], after_1959['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
#           edgecolor='black', linewidth=1)

plt.tight_layout()

# pdf = PdfPages("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis/" +
#                'Year_spreadOfDataBeforeAndAfter1984' + '.pdf')

# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()

plt.show()


""""
Wilcoxon Ranksums (all regions and for east and west separately --> Print out results to csv)
"""
#
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis/year_WilcoxonRanksums'
#           '.csv', 'wb') as file:
#     filewriter = csv.writer(file, delimiter=',')
#     filewriter.writerow(['Song Variable', 'All Regions w', 'All Regions p-value', 'East w', 'East p-value', 'West w',
#                          'West p-value'])
#     for sv in data_for_year.columns[4:]:
#         b = np.asarray(before_1984[sv])
#         a = np.asarray(after_1984[sv])
#         b_e = np.asarray(before_1984.loc[before_1984['Region'] == 'east', sv])
#         a_e = np.asarray(after_1984.loc[after_1984['Region'] == 'east', sv])
#         b_w = np.asarray(before_1984.loc[before_1984['Region'] == 'west', sv])
#         a_w = np.asarray(after_1984.loc[after_1984['Region'] == 'west', sv])
#         filewriter.writerow([sv, ranksums(b, a)[0], ranksums(b, a)[1], ranksums(b_e, a_e)[0], ranksums(b_e, a_e)[1],
#                             ranksums(b_w, a_w)[0], ranksums(b_w, a_w)[1]])

"""
Wilcoxon ranksums --> split into before and after 1984 and see if there is a difference in east and west within one 
of those categories
"""
# with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis'
#           '/year_WilcoxonRanksums_regionDiffsWithinTimeframe'
#           '.csv', 'wb') as file:
#     filewriter = csv.writer(file, delimiter=',')
#     filewriter.writerow(['Song Variable', 'Before 1984 w', 'Before 1984 p-value',
#                          'After 1984 w', 'After 1984  p-value'])
#     for sv in data_for_year.columns[4:]:
#         b = np.asarray(before_1984[sv])
#         a = np.asarray(after_1984[sv])
#         b_e = np.asarray(before_1984.loc[before_1984['Region'] == 'east', sv])
#         a_e = np.asarray(after_1984.loc[after_1984['Region'] == 'east', sv])
#         b_w = np.asarray(before_1984.loc[before_1984['Region'] == 'west', sv])
#         a_w = np.asarray(after_1984.loc[after_1984['Region'] == 'west', sv])
#         filewriter.writerow([sv, ranksums(b_e, b_w)[0], ranksums(b_e, b_w)[1],
#                              ranksums(a_e, a_w)[0], ranksums(a_e, a_w)[1]])

"""
Wilcoxon ranksums --> split into before and after 1959 and see if there is a difference in east and west within one 
of those categories
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis'
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