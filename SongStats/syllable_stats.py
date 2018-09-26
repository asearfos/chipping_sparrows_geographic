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
Frequency of syllable clusters
"""
my_dpi = 96
sns.set(style='white')
sns.set_context({"figure.figsize": (20, 7)})

# # raw counts (not normalized), sorted by total number of recordings in a cluster
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index().pivot(
#     columns='Region', index='ClusterNoAdjusted', values=0)
# freq_clusters['numInCluster'] = freq_clusters.sum(axis=1)
# freq_clusters = freq_clusters.sort_values(by='numInCluster', ascending=False)
# freq_clusters = freq_clusters.drop('numInCluster', axis=1)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black')
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_rawCounts_sortedByNumInCluster" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)

# # normalized by total number of recordings, don't use stacked (does not show regions)
# freq_clusters = combined_table.groupby(['ClusterNoAdjusted']).size().reset_index(name='count')
# num_of_recordings = combined_table.shape[0]
# freq_clusters['count'] = freq_clusters['count'].div(num_of_recordings)
# freq_clusters = freq_clusters.sort_values(by='count', ascending=False)
# ax = freq_clusters.plot(x='ClusterNoAdjusted', y='count', kind='bar', width=0.8, grid=None, fontsize=10, color='black',
#                         edgecolor='black')
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_normByTotalRecNum" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)

# # normalized by number of recordings in each region, sorted by region
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='ClusterNoAdjusted')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black')
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_normByRecNumInRegion_sortedByRegion" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)

# # normalized by number of recordings in each region, sorted by number of recordings in a cluster
# temp = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index().pivot(
#     columns='Region', index='ClusterNoAdjusted', values=0)
# temp['numInCluster'] = temp.sum(axis=1)
# temp = temp.sort_values(by='numInCluster', ascending=False)
# temp = temp.drop('numInCluster', axis=1)
# orderByNumInCluster = temp.index.values.tolist()
#
# freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='ClusterNoAdjusted')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters['clusters_cat'] = pd.Categorical(
#     freq_clusters.index.values,
#     categories=orderByNumInCluster,
#     ordered=True
# )
# freq_clusters = freq_clusters.sort_values('clusters_cat')
# freq_clusters = freq_clusters.drop('clusters_cat', axis=1)
# # freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)
# ax = freq_clusters.plot(kind='bar', stacked=False, width=1, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black')
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableFrequency_normByRecNumInRegion_sortedByNumInCluster_unstacked" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)
# quit()

"""
Frequency of syllable categories
"""
my_dpi = 96
sns.set(style='white')
sns.set_context({"figure.figsize": (20, 7)})

# # raw counts (not normalized), sorted by total number of recordings in a cluster
# freq_clusters = combined_table.groupby(['Region', 'Category']).size().reset_index().pivot(
#     columns='Region', index='Category', values=0)
# print(freq_clusters)
# freq_clusters['numInCategory'] = freq_clusters.sum(axis=1)
# freq_clusters = freq_clusters.sort_values(by='numInCategory', ascending=False)
# freq_clusters = freq_clusters.drop('numInCategory', axis=1)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black', rot=0)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableCategories_rawCounts_sortedByNumInCategory" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)


# # normalized by total number of recordings, don't use stacked (does not show regions)
# freq_clusters = combined_table.groupby(['Category']).size().reset_index(name='count')
# num_of_recordings = combined_table.shape[0]
# freq_clusters['count'] = freq_clusters['count'].div(num_of_recordings)
# freq_clusters = freq_clusters.sort_values(by='count', ascending=False)
# ax = freq_clusters.plot(x='Category', y='count', kind='bar', width=0.8, grid=None, fontsize=10, color='black',
#                         edgecolor='black', rot=0)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableCategories_normByTotalRecNum" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)


# # normalized by number of recordings in each region, sorted by region
# freq_clusters = combined_table.groupby(['Region', 'Category']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='Category')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black', rot=0)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableCategory_normByRecNumInRegion_sortedByRegion" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)


# # normalized by number of recordings in each region, sorted by number of recordings in a category
# temp = combined_table.groupby(['Region', 'Category']).size().reset_index().pivot(
#     columns='Region', index='Category', values=0)
# temp['numInCategory'] = temp.sum(axis=1)
# temp = temp.sort_values(by='numInCategory', ascending=False)
# temp = temp.drop('numInCategory', axis=1)
# orderByNumInCategory = temp.index.values.tolist()
#
# freq_clusters = combined_table.groupby(['Region', 'Category']).size().reset_index(name='count')
# num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
# freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
# freq_clusters = freq_clusters.pivot(columns='Region', index='Category')
# freq_clusters.columns = freq_clusters.columns.droplevel()
# freq_clusters['category_cat'] = pd.Categorical(
#     freq_clusters.index.values,
#     categories=orderByNumInCategory,
#     ordered=True
# )
# freq_clusters = freq_clusters.sort_values('category_cat')
# freq_clusters = freq_clusters.drop('category_cat', axis=1)
# # freq_clusters = freq_clusters.sort_values(by=['east', 'west', 'south', 'mid'], ascending=False)
# ax = freq_clusters.plot(kind='bar', stacked=True, width=0.8, grid=None, fontsize=10,
#                         color=['#1f78b4', 'gray', '#f17300', '#33a02c'], edgecolor='black', rot=0)
# plt.tight_layout()
# plt.savefig(
#     "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
#     "/SyllableCategory_normByRecNumInRegion_sortedByNumInCateogry" + '.pdf', type='pdf', bbox_inches='tight',
#     transparent=True)
"""
Two plots for paper
"""
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

sns.set_context({"figure.figsize": (10, 5)})
# group by decade and syllable cluster
clusters_over_time = combined_table.groupby([(combined_table.RecordingYear//10)*10, 'ClusterNoAdjusted']).size(
    ).reset_index(name='count')
num_rec_per_decade = clusters_over_time.groupby('RecordingYear')['count'].transform('sum')
clusters_over_time['count'] = clusters_over_time['count'].div(num_rec_per_decade)

most_freq_clusters = combined_table.groupby('ClusterNoAdjusted').size().sort_values(ascending=False).head(
    5).reset_index().ClusterNoAdjusted.values.tolist()
print(most_freq_clusters)

clusters_over_time_most_common = clusters_over_time[clusters_over_time['ClusterNoAdjusted'].isin(
    most_freq_clusters)].pivot(columns='ClusterNoAdjusted', index='RecordingYear')
# freq_clusters.columns = freq_clusters.columns.droplevel()
clusters_over_time_most_common.columns = clusters_over_time_most_common.columns.droplevel()
print(clusters_over_time_most_common)
ax = clusters_over_time_most_common.plot(kind='line', grid=None, fontsize=10)
plt.tight_layout()
plt.savefig(
    "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SyllableAnalysis"
    "/SyllablesOverDecades_normByRecNumInDecade_top5Clusters" + '.pdf', type='pdf',
    bbox_inches='tight',
    transparent=True)