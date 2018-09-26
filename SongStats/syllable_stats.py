from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy import stats
import numpy as np


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
Frequency of syllable clusters and syllable categories: Two plots for paper
"""
my_dpi = 96
sns.set(style='white')
sns.set_context({"figure.figsize": (20, 7)})

# # raw counts (not normalized)
#
# # sort by type (type with most to type with least); within type sort by cluster
# temp = combined_table.groupby(['Category']).size().reset_index(name='numInCategory')
# temp = temp.sort_values(by='numInCategory')
# orderByNumInCategory = temp.Category.values.tolist()
#
# temp2 = combined_table.groupby(['Category', 'ClusterNoAdjusted']).size().reset_index(name='numInCluster')
# temp2['Category'] = temp2.Category.astype('category', ordered=True, categories=orderByNumInCategory)
# temp2 = temp2.sort_values(['Category', 'numInCluster'], ascending=False)
# orderByCatThenByNumInCluster = temp2.ClusterNoAdjusted.values.tolist()
#
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count').pivot(
#     columns='Region', index='ClusterNoAdjusted')
# freq_clusters['clusters_cat'] = pd.Categorical(
#     freq_clusters.index.values,
#     categories=orderByCatThenByNumInCluster,
#     ordered=True
# )
# freq_clusters = freq_clusters.sort_values('clusters_cat')
# freq_clusters = freq_clusters.drop('clusters_cat', axis=1)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=1, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black')
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_counts_sortedByCatThenByNumInCluster" + '.pdf', type='pdf',
#     bbox_inches='tight',
#     transparent=True)
#
# # normalized by # recordings in each region
# # sort by type (type with most to type with least); within type sort by cluster
# freq_clusters = combined_table.groupby(['Region', 'Category']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='Category')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters['category_cat'] = pd.Categorical(
#     freq_clusters.index.values,
#     categories=orderByNumInCategory[::-1],
#     ordered=True
# )
# freq_clusters = freq_clusters.sort_values('category_cat')
# freq_clusters = freq_clusters.drop('category_cat', axis=1)
# print(freq_clusters)
# freq_clusters = freq_clusters.reindex_axis(['east', 'west', 'south', 'mid'], axis=1)
# print(freq_clusters)
# ax = freq_clusters.plot(kind='bar', stacked=False, width=0.5, grid=None, fontsize=10,
#                         color=['#1f78b4', '#33a02c', '#f17300', 'gray'], edgecolor='black', rot=0)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableCategory_normByRecNumInRegion_sortedByCatThenByNumInCluster" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)


"""
Syllables over time (by decades)
"""
my_dpi = 96
sns.set(style='white')
# sns.set_context({"figure.figsize": (5, 20)})

# # group by decade and syllable cluster
# clusters_over_time = combined_table.groupby([(combined_table.RecordingYear//10)*10, 'ClusterNoAdjusted']).size(
#     ).reset_index(name='count')
#
# # control for number of recordings in each decade
# num_rec_per_decade = clusters_over_time.groupby('RecordingYear')['count'].transform('sum')
# clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_decade)
# # control for number of recordings in each syllable cluster
# num_rec_per_cluster = clusters_over_time.groupby('ClusterNoAdjusted')['count'].transform('sum')
# clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_cluster)
#
#
# clusters_over_time = clusters_over_time[clusters_over_time['count'] != 1]  # remove any sylls only in one decade
# clusters_over_time = clusters_over_time.pivot(columns='RecordingYear', index='ClusterNoAdjusted').fillna(0)
# ax = sns.heatmap(clusters_over_time, xticklabels=True, yticklabels=True, annot=True)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableHeatmap_byDecade_normDecadeThenCluster" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)
# plt.show()




# sns.set_context({"figure.figsize": (10, 5)})
# # group by decade and syllable cluster
# clusters_over_time = combined_table.groupby([(combined_table.RecordingYear//10)*10, 'ClusterNoAdjusted']).size(
#     ).reset_index(name='count')
# num_rec_per_decade = clusters_over_time.groupby('RecordingYear')['count'].transform('sum')
# clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_decade)
#
# most_freq_clusters = combined_table.groupby('ClusterNoAdjusted').size().sort_values(ascending=False).head(
#     5).reset_index().ClusterNoAdjusted.values.tolist()
#
# # print(clusters_over_time[clusters_over_time['ClusterNoAdjusted'].isin(most_freq_clusters)].sort_values(
# #     ['ClusterNoAdjusted', 'RecordingYear']))
#
#
# clusters_over_time_most_common = clusters_over_time[clusters_over_time['ClusterNoAdjusted'].isin(
#     [35, 75, 7])].pivot(columns='ClusterNoAdjusted', index='RecordingYear')
# # freq_clusters.columns = freq_clusters.columns.droplevel()
# clusters_over_time_most_common.columns = clusters_over_time_most_common.columns.droplevel()
# ax = clusters_over_time_most_common.plot(kind='line', grid=None, fontsize=10)
# plt.tight_layout()
# plt.show()
#
# # combined_table.RecordingYear = (combined_table.RecordingYear//10)*10
# # print(combined_table[combined_table['ClusterNoAdjusted'].isin([75])][['CatalogNo', 'RecordingYear',
# #                                                                       'ClusterNoAdjusted', 'Latitude', 'Longitude']])
#
# # plt.savefig(
# #     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
# #     "/SyllablesOverDecades_normByRecNumInDecade_testing" + '.pdf', type='pdf',
# #     bbox_inches='tight',
# #     transparent=True)





# before vs after 1984
sns.set_context({"figure.figsize": (5, 6)})
# group by decade and syllable cluster
most_freq_clusters = combined_table.groupby('ClusterNoAdjusted').size().sort_values(ascending=False).head(
    10).reset_index().ClusterNoAdjusted.values.tolist()

combined_table['1984'] = np.where(combined_table['RecordingYear'] < 1984, 'before', 'after')
clusters_over_time = combined_table.groupby(['1984', 'ClusterNoAdjusted']).size(
    ).reset_index(name='count')
print(clusters_over_time[clusters_over_time['ClusterNoAdjusted'].isin(most_freq_clusters)].sort_values(
    ['ClusterNoAdjusted']))

# normalize by the total number of recordings either before or after 1984.
num_rec_per_group = clusters_over_time.groupby('1984')['count'].transform('sum')
clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_group)


clusters_over_time_most_common = clusters_over_time[clusters_over_time['ClusterNoAdjusted'].isin(
    most_freq_clusters)]

sns.set(style='white', rc={"font.style": "normal", 'lines.markersize': 2})
ax = sns.pointplot(x='1984', y='count', hue='ClusterNoAdjusted', data=clusters_over_time_most_common,
                   order=['before', 'after'], palette=['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
                                                      '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a'])

plt.tight_layout()
# plt.show()

plt.savefig(
    "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
    "/SyllablesBeforeAfter1984_normByRecNumInGroup" + '.pdf', type='pdf',
    bbox_inches='tight',
    transparent=True)