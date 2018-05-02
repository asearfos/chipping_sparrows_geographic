import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy import stats, spatial
import datetime
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

"""
Load data and organize/subset for PCA and procrustes testing
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_for_PCA = log_song_data_unique.drop(col_to_skip, axis=1)

"""
PCA analysis to see which song variable explain most of the variance
"""
songVarTable_forPCA = StandardScaler().fit_transform(data_for_PCA.drop(['Region', 'Latitude', 'Longitude'], axis=1))
# print(songVarTable_forPCA)
# choosing number of components
# pca = PCA()
# PCs = pca.fit_transform(songVarTable_forPCA)
# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance')
# plt.show()
# print(np.shape(PCs))

pca = PCA(n_components=2)
PCs = pca.fit_transform(songVarTable_forPCA)
# principalDf = pd.DataFrame(data=PCs, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
principalDf = pd.DataFrame(data=PCs, columns=['PC1', 'PC2'])
finalDf = pd.concat([data_for_PCA[['Region', 'Latitude', 'Longitude']], principalDf], axis=1)
# print(finalDf)
# print(finalDf.shape)
# print(principalDf.shape)
# print(pca.explained_varianc  e_ratio_)


# Plot
# sns.set(style='white')
# pca_plot = sns.lmplot(x='PC1', y='PC2', data=finalDf[['Region', 'PC1', 'PC2']], fit_reg=False, hue='Region',
#                       legend_out=False)
# ax = pca_plot.axes
# ax[0, 0].set_ylabel('PC2', fontsize=50)
# ax[0, 0].set_xlabel('PC1', fontsize=50)
# ax[0, 0].tick_params(labelsize=40)
# leg = pca_plot.axes[0, 0].get_legend()
# leg.set_title(None)
# labs = leg.texts
# labs[0].set_fontsize(30)
# labs[1].set_fontsize(30)
# plt.show()

# run procrustes
stand_latlong, oriented_pcs, disparity = spatial.procrustes(data1=finalDf[['Longitude', 'Latitude']], data2=finalDf[[
    'PC1', 'PC2']])
print('my disparity: ', disparity)
# print('mean: ', stand_latlong.mean(0))
# print('std: ', stand_latlong.std(0))
oriented_pcs_df = pd.DataFrame(data=oriented_pcs, index=None, columns=['PC1_oriented', 'PC2_oriented'])
oriented_pcs_df = pd.concat([finalDf[['Region']], oriented_pcs_df], axis=1).copy()
#
# # Plot adjusted PCs to latitude and longitude axes
# sns.set(style='white')
# pca_plot_oriented = sns.lmplot(x='PC1_oriented', y='PC2_oriented', data=oriented_pcs_df, fit_reg=False, hue='Region',
#                       legend_out=False)
# ax = pca_plot_oriented.axes
# ax[0, 0].set_ylabel('PC2', fontsize=50)
# ax[0, 0].set_xlabel('PC1', fontsize=50)
# ax[0, 0].tick_params(labelsize=40)
# leg = pca_plot_oriented.axes[0, 0].get_legend()
# leg.set_title(None)
# labs = leg.texts
# labs[0].set_fontsize(30)
# labs[1].set_fontsize(30)
# plt.show()

# # run procrustes 100,000x to get empirical p-value
# all_disparities = [None]*100000
# for i in range(100000):
#     _, _, all_disparities[i] = spatial.procrustes(data1=finalDf[['Longitude', 'Latitude']].sample(frac=1).reset_index(
#         drop=True), data2=finalDf[['PC1', 'PC2']])
#
# print('here')
# print(sorted(all_disparities)[0])
# print(sorted(all_disparities)[-1])
