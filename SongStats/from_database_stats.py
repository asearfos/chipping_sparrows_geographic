import pandas as pd
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
import csv
from scipy.stats import ranksums

"""
Load data and organize/subset for testing differences in song variables 
between databases 
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis and any missing data
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay']
data_for_source = log_song_data_unique.drop(col_to_skip, axis=1)
data_for_source['RecordingTime'] = pd.to_datetime(data_for_source['RecordingTime'])
data_for_source['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_source['RecordingTime']]

#divide up by database
fromXC = data_for_source[data_for_source.FromDatabase == 'Xeno-Canto']
fromML = data_for_source.loc[data_for_source['FromDatabase'].isin(['Macaulay Library', 'eBird'])].copy().reset_index()
fromBL = data_for_source[data_for_source.FromDatabase == 'Borror Laboratory of Bioacoustics']
fromWC = data_for_source[data_for_source.FromDatabase == 'Wan-chun Liu']

""""
Wilcoxon Ranksums for 16 song variables ONLY FOR EAST SONGS
"""

fromXC_east = fromXC[fromXC.Region == 'east']
fromML_east = fromML[fromML.Region == 'east']
fromBL_east = fromBL[fromBL.Region == 'east']
fromWC_east = fromWC[fromWC.Region == 'east']

print(fromXC_east.shape)
print(fromML_east.shape)
print(fromBL_east.shape)
print(fromWC_east.shape)

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions/DatabaseAnalysis'
          '/databaseEastOnly_songProp_WilcoxonRanksums_XC.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'XC vs ML p-value',
                         'XC vs BL p-value',
                         'XC vs WC p-value'])

    for sv in data_for_source.columns[7:]:
        xc = np.asarray(fromXC_east[sv])
        ml = np.asarray(fromML_east[sv])
        bl = np.asarray(fromBL_east[sv])
        wc = np.asarray(fromWC_east[sv])
        filewriter.writerow([sv,
                             ranksums(xc, ml)[1],
                             ranksums(xc, bl)[1],
                             ranksums(xc, wc)[1]
                             ])

