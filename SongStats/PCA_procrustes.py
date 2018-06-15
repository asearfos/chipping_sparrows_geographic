import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import csv
from scipy import stats, spatial
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

"""
Load data and organize/subset for PCA and procrustes testing
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_for_PCA = log_song_data_unique.drop(col_to_skip, axis=1)

"""
PCA analysis
"""
# temporarily do not need Region, Latitude and Longitude for PCA, will need later for plotting (color based by region)
songVarTable_forPCA = StandardScaler().fit_transform(data_for_PCA.drop(['Region', 'Latitude', 'Longitude'], axis=1))

# Visualize Explained Variance
# note for the plot, the PC1 is really at the 0 tick mark as python counts from 0
# pca = PCA()
# PCs = pca.fit_transform(songVarTable_forPCA)
# print('explained variance')
# print(pca.explained_variance_ratio_)
# print('end')
# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance')
# plt.show()

# Calculate the first 2 PC's
pca = PCA(n_components=2)
PCs_nComp = pca.fit_transform(songVarTable_forPCA)
principalDf = pd.DataFrame(data=PCs_nComp, columns=['PC1', 'PC2'])
finalDf = pd.concat([data_for_PCA[['Region', 'Latitude', 'Longitude']], principalDf], axis=1)
print(pca.explained_variance_ratio_)

# Plot square figure
sns.set(style='white',
        rc={"font.style": "normal",
            'axes.labelsize': 30,
            'figure.figsize': (12.0, 12.0),
            'xtick.labelsize': 25,
            'ytick.labelsize': 25})

pca_plot = sns.lmplot(x='PC1', y='PC2', data=finalDf[['Region', 'PC1', 'PC2']], fit_reg=False, hue='Region',
                      legend_out=False, scatter_kws={'alpha': 0.3, 's': 200},
                      palette=['#f17300', '#1f78b4', '#542788', '#33a02c'], size=10, aspect=1)

leg = pca_plot.axes[0, 0].get_legend()
leg.set_title(None)
labs = leg.texts
labs[0].set_fontsize(30)
labs[1].set_fontsize(30)
plt.show()

# save figure
pca_plot.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\PCA_Procrustes'
                 '\PCA_scatter_squarePlot_forPaper.pdf')

# Plot rectangular figure
sns.set(style='white',
        rc={"font.style": "normal",
            'axes.labelsize': 30,
            'figure.figsize': (12.0, 12.0),
            'xtick.labelsize': 25,
            'ytick.labelsize': 25})

pca_plot = sns.lmplot(x='PC1', y='PC2', data=finalDf[['Region', 'PC1', 'PC2']], fit_reg=False, hue='Region',
                      legend_out=False, scatter_kws={'alpha': 0.3, 's': 200},
                      palette=['#f17300', '#1f78b4', '#542788', '#33a02c'], size=10, aspect=1.5)

leg = pca_plot.axes[0, 0].get_legend()
leg.set_title(None)
labs = leg.texts
labs[0].set_fontsize(30)
labs[1].set_fontsize(30)
plt.show()

# save figure
pca_plot.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\PCA_Procrustes'
                 '\PCA_scatter_rectanglePlot_forPaper.pdf')


"""
Procrustes analysis
"""
# run procrustes
stand_latlong, oriented_pcs, disparity_of_data = spatial.procrustes(data1=finalDf[['Longitude', 'Latitude']],
data2=finalDf[[
    'PC1', 'PC2']])
print('my disparity: ', disparity_of_data)

# run procrustes 100,000x to get empirical p-value
n = 100000
all_disparities = [None]*n
for i in range(100000):
    _, _, all_disparities[i] = spatial.procrustes(data1=finalDf[['Longitude', 'Latitude']].sample(frac=1).reset_index(
        drop=True), data2=finalDf[['PC1', 'PC2']])

smallest_disparity = sorted(all_disparities)[-1]
print(sorted(all_disparities)[0])
print(sorted(all_disparities)[-1])

# calculate empirical p-value
# disparity is the sum of the squares of the pointwise differences between the two input datasets
# disparity is what the algorithm tries to minimize
# therefore, p=r/n where n is number of replicates, r is number of test statistics < that calculated for the actual data
i = 0
count = 0
while all_disparities[i] < disparity_of_data:
    count += 1

p = count/n

with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\PCA_Procrustes'
          '\PCA_Procrustes_Output.txt', 'wb') as output_file:
    output_file.write('Explained Variance for PC1 and PC2: ' + str(pca.explained_variance_ratio_) + '\r')
    output_file.write('Disparity of Data: ' + str(disparity_of_data) + '\r')
    output_file.write('p-value for n=' + str(n) + ': ' + str(p))
output_file.close()
