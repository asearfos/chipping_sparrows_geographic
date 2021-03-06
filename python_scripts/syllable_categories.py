from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import seaborn as sns; sns.set()

"""
Load in song data
"""

# song meta data
data_path1 = 'C:/Users/abiga\Box ' \
             'Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path1, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# get rid of unnecessary metadata and the song stat variables
col_to_skip = ['FromDatabase', 'ComparedStatus', 'RecordingDay',
               'RecordingMonth'] + list(log_song_data_unique.columns[
                                        10:26].values)
song_info = log_song_data_unique.drop(col_to_skip, axis=1)

"""
Load in syllable cluster data
"""
# syllable clusters
data_path2 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject" \
             "\StatsOfFinalData_withReChipperReExported" \
             "\AnimalBehaviourRevisions\SyllableAnalysis" \
             "\SyllableClusters_820UniqueUse.csv"

cluster_data = pd.DataFrame.from_csv(data_path2, header=0, index_col=None)

col_to_skip2 = ['SyllableNumber', 'ClusterNo']
cluster_data = cluster_data.drop(col_to_skip2, axis=1)
cluster_data['ClusterNoAdjusted'] = cluster_data['ClusterNoAdjusted'].astype(int)

"""
combine tables using CatalogNo
"""
combined_table = song_info.merge(cluster_data, how='inner', on='CatalogNo')
combined_table = combined_table.drop_duplicates(['CatalogNo', 'ClusterNoAdjusted'], keep='first')
combined_table = combined_table.drop(['FileName'], axis=1)

print(combined_table.shape)
print(combined_table.groupby('Region').count())
quit()

"""
Frequency of syllable clusters and syllable categories: Two plots for paper
"""
my_dpi = 96
sns.set(style='white')
sns.set_style('ticks')
sns.set_context({"figure.figsize": (20, 7)})


# for the legend, get the total number of recordings in each region
print(combined_table.groupby('Region').size().reset_index(name='count')[['Region', 'count']])
combined_table.groupby(
    'Region').size().reset_index(name='count')[['Region', 'count']].to_csv(
    'C:/Users/abiga\Box '
    'Sync\Abigail_Nicole\ChippiesProject'
    '\StatsOfFinalData_withReChipperReExported/AnimalBehaviourRevisions'
    '/SyllableAnalysis/RegionRecordingCountsForLegend.csv')

# get order of syllable categories from ones with most to least number of recordings
temp = combined_table.groupby(['Category']).size().reset_index(name='numInCategory')
temp = temp.sort_values(by='numInCategory')
orderByNumInCategory = temp.Category.values.tolist()

# within syllable category, get the order of syllable clusters from ones with most to least number of recordings
temp2 = combined_table.groupby(['Category', 'ClusterNoAdjusted']).size().reset_index(name='numInCluster')
temp2['Category'] = temp2.Category.astype('category', ordered=True, categories=orderByNumInCategory)
temp2 = temp2.sort_values(['Category', 'numInCluster'], ascending=False)
orderByCatThenByNumInCluster = temp2.ClusterNoAdjusted.values.tolist()

#####PLOT 1
# raw counts (not normalized)
# sort by type (type with most to type with least); within type sort by cluster with most to least
# stack counts in regions
freq_clusters = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size().reset_index(name='count').pivot(
    columns='Region', index='ClusterNoAdjusted')
# use the previously found order to order the cluster numbers
freq_clusters['clusters_cat'] = pd.Categorical(
    freq_clusters.index.values,
    categories=orderByCatThenByNumInCluster,
    ordered=True
)
freq_clusters = freq_clusters.sort_values('clusters_cat')
freq_clusters = freq_clusters.drop('clusters_cat', axis=1)


# plot and save
ax = freq_clusters.plot(kind='bar',
                        stacked=True,
                        width=1,
                        grid=None,
                        fontsize=10,
                        color=['#1f78b4', 'gray', '#f17300', '#33a02c'],
                        edgecolor='black')
plt.tight_layout()
plt.savefig(
    "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
    "\StatsOfFinalData_withReChipperReExported"
    "/AnimalBehaviourRevisions/SyllableAnalysis"
    "/SyllableFrequency_counts_sortedByCatThenByNumInCluster" + '.pdf',
    type='pdf', bbox_inches='tight', transparent=True)

#####PLOT 2
# normalized by # recordings in each region
# sort by type (type with most to type with least); within type sort by cluster

# group by region and syllable category
freq_clusters = combined_table.groupby(['Region', 'Category']).size().reset_index(name='count')

# control for number of recordings per region
num_rec_per_region = freq_clusters.groupby('Region')['count'].transform('sum')
freq_clusters['count'] = freq_clusters['count'].div(num_rec_per_region)
freq_clusters = freq_clusters.pivot(columns='Region', index='Category')
freq_clusters.columns = freq_clusters.columns.droplevel()

# sort the categories from one with most recordings to least
freq_clusters['category_cat'] = pd.Categorical(
    freq_clusters.index.values,
    categories=orderByNumInCategory[::-1],
    ordered=True
)
freq_clusters = freq_clusters.sort_values('category_cat')
freq_clusters = freq_clusters.drop('category_cat', axis=1)

# sort the regions
freq_clusters = freq_clusters.reindex_axis(['south', 'west', 'mid', 'east'],
                                           axis=1)

# plot and save figure
ax = freq_clusters.plot(kind='bar',
                        stacked=False,
                        width=0.5,
                        grid=None,
                        fontsize=10,
                        color=['#f17300', '#33a02c', 'gray', '#1f78b4'],
                        edgecolor='black', rot=0)
plt.tight_layout()
plt.savefig(
    "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
    "\StatsOfFinalData_withReChipperReExported"
    "/AnimalBehaviourRevisions/SyllableAnalysis"
    "/SyllableCategory_normByRecNumInRegion_sortedByCatThenByNumInCluster" +
    '.pdf', type='pdf', bbox_inches='tight', transparent=True)

"""
Make an output table for supplement that give the total number of recordings in each syllable cluster, the earliest 
and latest observation of such syllable and number of such syllable recorded in the east, west, mid, south. 
"""

# get total number of recordings for each syllable cluster
cluster_num_rec = combined_table.groupby('ClusterNoAdjusted').size().reset_index(
    name='NumberOfRecordings').sort_values('ClusterNoAdjusted').set_index('ClusterNoAdjusted')

cluster_category = combined_table.drop_duplicates('ClusterNoAdjusted')[['ClusterNoAdjusted',
                                                                        'Category']].sort_values(
    'ClusterNoAdjusted').set_index('ClusterNoAdjusted')

earliest_latest_rec = combined_table.assign(EarliestYear=combined_table['RecordingYear'].abs(), LatestYear=combined_table[
    'RecordingYear'].abs()).groupby('ClusterNoAdjusted').agg({'EarliestYear': 'min', 'LatestYear': 'max'})
earliest_latest_rec = earliest_latest_rec.fillna(0).astype(int)

cluster_regional_spread = combined_table.groupby(['Region', 'ClusterNoAdjusted']).size()\
    .reset_index(name='num_in_region').pivot(columns='Region', index='ClusterNoAdjusted')
cluster_regional_spread.columns = cluster_regional_spread.columns.droplevel()
cluster_regional_spread = cluster_regional_spread.fillna(0).astype(int)

summary_table = pd.concat([cluster_num_rec, earliest_latest_rec,
                           cluster_regional_spread, cluster_category],
                          axis=1)
summary_table = summary_table.reindex_axis(['NumberOfRecordings',
                                            'EarliestYear', 'LatestYear',
                                            'east', 'west', 'south', 'mid',
                                            'Category'],
                                           axis=1)
summary_table.to_csv('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject'
                     '\StatsOfFinalData_withReChipperReExported'
                     '/AnimalBehaviourRevisions/SyllableAnalysis'
                     '/SyllableClusterSummaryTable.csv')
