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
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingYear', 'RecordingTime']
data_for_seasons = log_song_data_unique.drop(col_to_skip, axis=1).dropna(axis=0)

# divide as before and after summer solstice (June 21st, do not specify by year)
before_solstice = data_for_seasons.loc[(data_for_seasons['RecordingMonth'] <= 6) &
                                   (data_for_seasons['RecordingDay'] < 21), :].copy().reset_index()

after_solstice = data_for_seasons.loc[(data_for_seasons['RecordingMonth'] > 6) &
                                   (data_for_seasons['RecordingDay'] > 21), :].copy().reset_index()

"""
Histogram plot of the number of recordings per year
"""
sns.distplot(data_for_seasons['RecordingMonth'], bins=12)
plt.show()

"""
Location of data by before or after solstice 
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

#plot points at sampling locations
m.scatter(before_solstice['Longitude'], before_solstice['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
          edgecolor='black', linewidth=1)

#plot points at sampling locations
m.scatter(after_solstice['Longitude'], after_solstice['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
          edgecolor='black', linewidth=1)

plt.tight_layout()

plt.savefig("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported"
            "/SeasonsAnalysis/Seasons_spreadOfBeforeAfterData.pdf", type='pdf', dpi=fig.dpi, bbox_inches='tight')

# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()

plt.show()

""""
Wilcoxon Ranksums (all regions and for east and west separately --> Print out results to csv
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/SeasonsAnalysis'
          '/season_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'All Regions w', 'All Regions p-value', 'East w', 'East p-value', 'West w',
                         'West p-value'])
    for sv in data_for_seasons.columns[5:]:
        b = np.asarray(before_solstice[sv])
        a = np.asarray(after_solstice[sv])
        b_e = np.asarray(before_solstice.loc[before_solstice['Region'] == 'east', sv])
        a_e = np.asarray(after_solstice.loc[after_solstice['Region'] == 'east', sv])
        # b_w = np.asarray(before_solstice.loc[before_solstice['Region'] == 'west', sv])
        # a_w = np.asarray(after_solstice.loc[after_solstice['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b, a)[0], ranksums(b, a)[1], ranksums(b_e, a_e)[0], ranksums(b_e, a_e)[1]])

