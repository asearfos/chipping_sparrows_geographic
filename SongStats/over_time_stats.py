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
before_1985 = data_for_year[data_for_year.RecordingYear < 1985]
after_1985 = data_for_year[data_for_year.RecordingYear >= 1985]

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

#plot points at sampling locations with area proportional to number of samples at the location --> mtDNA
m.scatter(before_1985['Longitude'], before_1985['Latitude'], latlon=True, label=None, zorder=10, c='#dfc27d',
          edgecolor='black', linewidth=1)

#plot points at sampling locations with area proportional to number of samples at the location --> COI
m.scatter(after_1985['Longitude'], after_1985['Latitude'], latlon=True, label=None, zorder=10, c='#8c510a',
          edgecolor='black', linewidth=1)

plt.tight_layout()

# pdf = PdfPages("C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis/" +
#                'Year_spreadOfDataBeforeAndAfter1984' + '.pdf')

# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()

plt.show()


""""
Wilcoxon Ranksums (all regions and for east and west separately --> Print out results to csv
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/YearAnalysis/year_WilcoxonRanksums'
          '.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'All Regions w', 'All Regions p-value', 'East w', 'East p-value', 'West w',
                         'West p-value'])
    for sv in data_for_year.columns[4:]:
        b = np.asarray(before_1985[sv])
        a = np.asarray(after_1985[sv])
        b_e = np.asarray(before_1985.loc[before_1985['Region'] == 'east', sv])
        a_e = np.asarray(after_1985.loc[after_1985['Region'] == 'east', sv])
        b_w = np.asarray(before_1985.loc[before_1985['Region'] == 'west', sv])
        a_w = np.asarray(after_1985.loc[after_1985['Region'] == 'west', sv])
        filewriter.writerow([sv, ranksums(b, a)[0], ranksums(b, a)[1], ranksums(b_e, a_e)[0], ranksums(b_e, a_e)[1],
                            ranksums(b_w, a_w)[0], ranksums(b_w, a_w)[1]])
