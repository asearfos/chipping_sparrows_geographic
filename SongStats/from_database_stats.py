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
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay']
data_for_source = log_song_data_unique.drop(col_to_skip, axis=1).dropna(axis=0)
data_for_source['RecordingTime'] = pd.to_datetime(data_for_source['RecordingTime'])
data_for_source['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_source['RecordingTime']]

#divide up by database
fromXC = data_for_source[data_for_source.FromDatabase == 'Xeno-Canto']
fromML = data_for_source.loc[data_for_source['FromDatabase'].isin(['Macaulay Library', 'eBird'])].copy().reset_index()
fromBorrorWanChun = data_for_source[data_for_source.FromDatabase == 'old']

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

metadata = ['Latitude', 'Longitude', 'RecordingYear', 'RecordingMonth', 'RecordingTime']

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/DatabaseAnalysis/database_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Fixed Variable', 'XC vs MLeBird w', 'XC vs MLeBird p-value',
                         'XC vs Old w', 'XC vs Old p-value',
                         'Old vs MLeBird w', 'Old vs MLeBird p-value'])

    for sv in metadata:
        xc = np.asarray(fromXC[sv])
        ml = np.asarray(fromML[sv])
        old = np.asarray(fromBorrorWanChun[sv])
        filewriter.writerow([sv, ranksums(xc, ml)[0], ranksums(xc, ml)[1],
                             ranksums(xc, old)[0], ranksums(xc, old)[1],
                             ranksums(old, ml)[0], ranksums(old, ml)[1]])


"""
Box Plot for database
"""
data_for_source.FromDatabase.replace(['eBird'], ['Macaulay Library'], inplace=True)

for sv in metadata:
    fig = plt.figure(figsize=(7, 11))
    sns.set(style='white')
    ax = sns.boxplot(x='FromDatabase', y=sv, data=data_for_source[['FromDatabase', sv]], color='None',
                     fliersize=0, width=0.5, linewidth=2, order=['old', 'Xeno-Canto', 'Macaulay Library'])
    ax = sns.stripplot(x='FromDatabase', y=sv, data=data_for_source[['FromDatabase', sv]],
                       order=['old', 'Xeno-Canto', 'Macaulay Library'], size=7, jitter=True, lw=1, alpha=0.6,
                       edgecolor=None, linewidth=0)

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
                "/DatabaseAnalysis/" + sv + 'Database_OldXCML' + '.pdf', type='pdf', dpi=fig.dpi,
                bbox_inches='tight',
                transparent=True)
    # plt.show()

