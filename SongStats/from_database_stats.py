import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import csv
from mpl_toolkits.basemap import Basemap
from scipy.stats import ranksums

"""
Load data and organize/subset for testing differences in song variables between two databases (ML and XC)
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis and any missing data
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_for_source = log_song_data_unique.drop(col_to_skip, axis=1).dropna(axis=0)

#divide up by database
fromXC = data_for_source[data_for_source.FromDatabase == 'Xeno-Canto']
fromML = data_for_source.loc[data_for_source['FromDatabase'].isin(['Macaulay Library', 'eBird'])].copy().reset_index()

"""
Location of data, colored by database
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
m.scatter(fromXC['Longitude'], fromXC['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
          edgecolor='black', linewidth=1)

#plot points at sampling locations
m.scatter(fromML['Longitude'], fromML['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
          edgecolor='black', linewidth=1)

plt.tight_layout()

plt.savefig("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported"
            "/DatabaseAnalysis/Database_geoSpreadOfData_XCLightMLeBirdDark.pdf", type='pdf', dpi=fig.dpi,
            bbox_inches='tight')

plt.show()

""""
Wilcoxon Ranksums
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/DatabaseAnalysis/database_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'XC vs MLeBird w', 'XC vs MLeBird p-value'])

    for sv in (['Longitude'] + data_for_source.columns[4:].tolist()):
        b = np.asarray(fromXC[sv])
        a = np.asarray(fromML[sv])
        filewriter.writerow([sv, ranksums(b, a)[0], ranksums(b, a)[1]])
