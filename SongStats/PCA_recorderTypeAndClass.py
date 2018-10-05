import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import seaborn as sns; sns.set()
import csv
from scipy import stats, spatial
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Ellipse

"""
Load song and recorder type data, organize/subset for testing differences in recorder type
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis and any missing data
col_to_skip = ['FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear',
               'RecordingTime', 'Region', 'Latitude', 'Longitude']
data_for_song = log_song_data_unique.drop(col_to_skip, axis=1).dropna(axis=0)
fn = lambda x: x['CatalogNo'].split('.')[0]
data_for_song['CatalogNo'] = data_for_song.apply(fn, axis=1).astype(str)

# load recorder data
recorder_path = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject/recorder spreadsheets from nicole/recorder " \
                "data plus eBird.csv"
data_for_rec = pd.DataFrame.from_csv(recorder_path, header=0, index_col=None)
data_for_rec['CatalogNo'] = data_for_rec['catalogNumber'].astype(str)

# combine tables using CatalogNo
data_for_PCA = data_for_song.merge(data_for_rec, how='inner', on='CatalogNo')
data_for_PCA = data_for_PCA.drop(['CatalogNo', 'institutionCode', 'dateIdentified', 'recording_recorder'], axis=1)


"""
PCA analysis
"""
# temporarily do not need Region, Latitude, Longitude, RecordingYear or RecordingTime for PCA, will need later for
# correlations and plotting (color based by region)

songVarTable_forPCA = StandardScaler().fit_transform(data_for_PCA.drop(['recorder_type', 'recorder_class'], axis=1))


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
principalDf = pd.DataFrame(data=PCs_nComp, columns=['PC1', 'PC2'])  #multiply the PC1 and PC2 by -1 so that they
principalDf['PC1'] = -1*principalDf['PC1']

finalDf = pd.concat([data_for_PCA[['recorder_type', 'recorder_class']], principalDf], axis=1)
print(pca.explained_variance_ratio_)

"""
Plotting settings
"""

sns.set(style='white',
        rc={"font.style": "normal",
            'axes.labelsize': 34,
            'xtick.labelsize': 24,
            'ytick.labelsize': 24,
            'figure.figsize': (11.69, 8.27)})

colors_type = {'Digital recorder': '#1f78b4', 'Reel-to-reel': '#33a02c', 'DAT digital tape recorder': '#542788',
               'Cassette recorder': '#f17300', 'nan': 'grey', 'Phone': 'pink'}
colors_signal = {'Digital': '#1f78b4', 'Analog': '#33a02c', 'nan': 'grey', 'Phone': 'pink'}

"""
Plot first and second PCs
"""

fig0, ax0 = plt.subplots()
for group in finalDf.recorder_type.unique():
    sdata = finalDf.loc[finalDf['recorder_type'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax0.scatter(sdata['PC1'], sdata['PC2'], color=colors_type.get(group), alpha=0.6, s=50, label=group, edgecolors=None,
                linewidth=0)
    # ax0.add_artist(e)

xlim = ax0.get_xlim()
ylim = ax0.get_ylim()
ax0.set_xlabel('PC1')
ax0.set_ylabel('PC2')
ax0.legend(loc='upper left')
# plt.show()

# # save figure
# fig0.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
#              '\PCA_Procrustes\PCA_scatter_PC1PC2AllRegions_forPaper.pdf', transparent=True)

""""
Plot scatter with Confidence Ellipses
"""

def get_cov_ellipse(cov, centre, nstd, **kwargs):
    """
    Return a matplotlib Ellipse patch representing the covariance matrix
    cov centred at centre and scaled by the factor nstd.

    """

    # Find and sort eigenvalues and eigenvectors into descending order
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # The anti-clockwise angle to rotate our ellipse by
    vx, vy = eigvecs[:, 0][0], eigvecs[:, 0][1]
    theta = np.arctan2(vy, vx)

    # Width and height of ellipse to draw
    width, height = 2 * nstd * np.sqrt(eigvals)
    return Ellipse(xy=centre, width=width, height=height,
                   angle=np.degrees(theta), **kwargs)

fig1, ax1 = plt.subplots()
for group in finalDf.recorder_type.unique():
    sdata = finalDf.loc[finalDf['recorder_type'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax1.scatter(sdata['PC1'], sdata['PC2'], color=colors_type.get(group), alpha=0.6, s=50, label=group,
                edgecolors=None,
                linewidth=0)
    e = get_cov_ellipse(cov, (PC1_mean, PC2_mean), 2,
                        fc=colors_type.get(group), alpha=0.4)
    ax1.add_artist(e)

ax1.set_xlim(xlim[0], xlim[1])
ax1.set_ylim(ylim[0], ylim[1])
ax1.set_xlabel('PC1')
ax1.set_ylabel('PC2')
ax1.legend(loc='upper left')

# # save figure
# fig1.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
#              '\PCA_Procrustes\PCA_scatter_PC1PC2EastWestEllipses_forPaper.pdf', transparent=True)



"""
Plot first and second PCs
"""

fig0, ax0 = plt.subplots()
for group in finalDf.recorder_class.unique():
    sdata = finalDf.loc[finalDf['recorder_class'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax0.scatter(sdata['PC1'], sdata['PC2'], color=colors_signal.get(group), alpha=0.6, s=50, label=group, edgecolors=None,
                linewidth=0)
    # ax0.add_artist(e)

xlim = ax0.get_xlim()
ylim = ax0.get_ylim()
ax0.set_xlabel('PC1')
ax0.set_ylabel('PC2')
ax0.legend(loc='upper left')
# plt.show()

# # save figure
# fig0.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
#              '\PCA_Procrustes\PCA_scatter_PC1PC2AllRegions_forPaper.pdf', transparent=True)

""""
Plot scatter with Confidence Ellipses
"""

def get_cov_ellipse(cov, centre, nstd, **kwargs):
    """
    Return a matplotlib Ellipse patch representing the covariance matrix
    cov centred at centre and scaled by the factor nstd.

    """

    # Find and sort eigenvalues and eigenvectors into descending order
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # The anti-clockwise angle to rotate our ellipse by
    vx, vy = eigvecs[:, 0][0], eigvecs[:, 0][1]
    theta = np.arctan2(vy, vx)

    # Width and height of ellipse to draw
    width, height = 2 * nstd * np.sqrt(eigvals)
    return Ellipse(xy=centre, width=width, height=height,
                   angle=np.degrees(theta), **kwargs)

fig1, ax1 = plt.subplots()
for group in finalDf.recorder_class.unique():
    sdata = finalDf.loc[finalDf['recorder_class'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax1.scatter(sdata['PC1'], sdata['PC2'], color=colors_signal.get(group), alpha=0.6, s=50, label=group,
                edgecolors=None,
                linewidth=0)
    e = get_cov_ellipse(cov, (PC1_mean, PC2_mean), 2,
                        fc=colors_signal.get(group), alpha=0.4)
    ax1.add_artist(e)

ax1.set_xlim(xlim[0], xlim[1])
ax1.set_ylim(ylim[0], ylim[1])
ax1.set_xlabel('PC1')
ax1.set_ylabel('PC2')
ax1.legend(loc='upper left')
plt.show()

# # save figure
# fig1.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
#              '\PCA_Procrustes\PCA_scatter_PC1PC2EastWestEllipses_forPaper.pdf', transparent=True)
