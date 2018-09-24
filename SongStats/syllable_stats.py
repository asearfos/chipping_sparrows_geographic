from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy import stats
import numpy.ma as ma
import time


"""
Load in syllable cluster data
"""

# song meta data
data_path1 = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path1, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

col_to_skip = ['FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth']
song_info = log_song_data_unique.drop(col_to_skip, axis=1)

# syllable clusters
data_path2 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\ClusterSyllables" \
            "\PossiblyForPaper\SyllableClusters.csv"
cluster_data = pd.DataFrame.from_csv(data_path2, header=0, index_col=None)
cluster_data = cluster_data[cluster_data.CatalogNo != '192108']
cluster_data = cluster_data[cluster_data.CatalogNo != '65614601']
cluster_data = cluster_data.drop_duplicates('CatalogNo', keep='first')

col_to_skip2 = ['FileName', 'SyllableNumber', 'ClusterNo']
cluster_data = cluster_data.drop(col_to_skip2, axis=1)
cluster_data['ClusterNoAdjusted'] = cluster_data['ClusterNoAdjusted'].fillna(0).astype(int)


# combine tables using CatalogNo
combined_table = song_info.merge(cluster_data, how='inner', on='CatalogNo')



"""
Frequency of syllable type between regions
"""
my_dpi = 96
sns.set(style='white')
sns.set_context({"figure.figsize": (20, 7)})

# # raw counts, sorted by region
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index().pivot(columns='Region',
#                                                                                              index='ClusterNoAdjusted',
#                                                                                              values=0).sort_values(
#     by=['east', 'west', 'south', 'mid'], ascending=False)

# # normalized by number of recordings in each region, sorted by region
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='ClusterNoAdjusted')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)


# # normalized by total number of recordings, sorted by region
freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count')
num_of_recordings = combined_table.shape[0]
freq_clusters['count'] = freq_clusters['count'].div(num_of_recordings)
freq_clusters = freq_clusters.pivot(columns='Region', index='ClusterNoAdjusted')
freq_clusters.columns = freq_clusters.columns.droplevel()
freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)



ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10, color=['#1f78b4', 'gray',
                                                                                            '#f17300', '#33a02c'],
                        edgecolor='black')

# ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()

# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_sortedByEastWestSouthMid" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)
#
plt.show()
quit()

"""
Syllables over time (by decades)
"""
clusters_over_time = combined_table.groupby([(combined_table.RecordingYear//10)*10, 'ClusterNoAdjusted']).size(
    ).reset_index(name='count')
num_rec_per_cluster = clusters_over_time.groupby('ClusterNoAdjusted')['count'].transform('sum')
clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_cluster)
clusters_over_time = clusters_over_time[clusters_over_time['count'] != 1]  # remove any sylls only in one decade
clusters_over_time = clusters_over_time.pivot(columns='RecordingYear', index='ClusterNoAdjusted').fillna(0)

ax = sns.heatmap(clusters_over_time, xticklabels=True, yticklabels=True, square=True)
plt.show()