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
Load data and organize/subset for PCA and procrustes testing
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)
print(log_song_data.shape)

# remove all duplicate birdsongs
# keep unique and use (which is the one I choose if there were multiples from the same bird)
log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

# drop any metadata that is not needed for this analysis
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth']
data_for_PCA = log_song_data_unique.drop(col_to_skip, axis=1)
data_for_PCA['RecordingTime'] = pd.to_datetime(data_for_PCA['RecordingTime'])
data_for_PCA['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_PCA['RecordingTime']]

"""
PCA analysis
"""
# temporarily do not need Region, Latitude, Longitude, RecordingYear or RecordingTime for PCA, will need later for
# correlations and plotting (color based by region)
songVarTable_forPCA = StandardScaler().fit_transform(data_for_PCA.drop(['Region', 'Latitude', 'Longitude',
                                                                        'RecordingYear', 'RecordingTime'], axis=1))

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

finalDf = pd.concat([data_for_PCA[['Region', 'Latitude', 'Longitude']], principalDf], axis=1)
print(pca.explained_variance_ratio_)

# output the loadings
col = data_for_PCA.drop(['Region', 'Latitude', 'Longitude',
                         'RecordingYear', 'RecordingTime'], axis=1).columns
loadings = pd.DataFrame(pca.components_, columns=col,
                   index=['PC1', 'PC2'])
print(loadings.T)
loadings.T.to_csv('C:/Users/abiga/Box '
               'Sync/Abigail_Nicole/ChippiesProject'
               '/StatsOfFinalData_withReChipperReExported/PCA_Procrustes'
               '/PCA_loadings.csv')

quit()
"""
PC1 and PC2 correlation to song variables
"""
data_for_corr = data_for_PCA.drop(['Region'], axis=1)

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/PCA_Procrustes/PCA_songVar_corr.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'PC1 r',
                         'PC1 pval',
                         'PC2 r',
                         'PC2 pval'])

    for var in data_for_corr.columns.values[:]:
        # find any rows that do not have the var; remove such rows from both x and y.
        x = data_for_corr[var]
        nas = x.isnull()
        y = finalDf[~nas]
        r1, pval1 = stats.pearsonr(x=x[~nas], y=y['PC1'])
        r2, pval2 = stats.pearsonr(x=x[~nas], y=y['PC2'])
        filewriter.writerow([var, r1, pval1, r2, pval2])

"""
Plotting settings
"""

sns.set(style='white',
        rc={"font.style": "normal",
            'axes.labelsize': 34,
            'xtick.labelsize': 24,
            'ytick.labelsize': 24,
            'figure.figsize': (11.69, 8.27)})

colors = {'east': '#1f78b4', 'west': '#33a02c', 'mid': '#542788', 'south': '#f17300'}

"""
Plot first and second PCs
"""

fig0, ax0 = plt.subplots()
for group in finalDf.Region.unique():
    sdata = finalDf.loc[finalDf['Region'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax0.scatter(sdata['PC1'], sdata['PC2'], color=colors.get(group), alpha=0.6, s=50, label=group, edgecolors=None, linewidth=0)
    # ax0.add_artist(e)

xlim = ax0.get_xlim()
ylim = ax0.get_ylim()
ax0.set_xlabel('PC1')
ax0.set_ylabel('PC2')
ax0.legend(loc='upper left')
plt.show()


# save figure
fig0.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
             '\PCA_Procrustes\PCA_scatter_PC1PC2AllRegions_forPaper.pdf', transparent=True)

""""
Plot scatter with Confidence Ellipses
"""

# function adapted from https://scipython.com/book/chapter-7-matplotlib/examples/bmi-data-with-confidence-ellipses/
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
for group in ['east', 'west']:
    sdata = finalDf.loc[finalDf['Region'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax1.scatter(sdata['PC1'], sdata['PC2'], color=colors.get(group), alpha=0.6, s=50, label=group, edgecolors=None, linewidth=0)
    e = get_cov_ellipse(cov, (PC1_mean, PC2_mean), 2,
                        fc=colors.get(group), alpha=0.4)
    ax1.add_artist(e)

ax1.set_xlim(xlim[0], xlim[1])
ax1.set_ylim(ylim[0], ylim[1])
ax1.set_xlabel('PC1')
ax1.set_ylabel('PC2')
ax1.legend(loc='upper left')
plt.show()

# save figure
fig1.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
             '\PCA_Procrustes\PCA_scatter_PC1PC2EastWestEllipses_forPaper.pdf', transparent=True)

""""
Plot points at mean locations proportional to number of samples
"""

fig2, ax2 = plt.subplots()
for group in finalDf.Region.unique()[::-1]:
    sdata = finalDf.loc[finalDf['Region'].isin([group])]
    PC1_mean = np.mean(sdata['PC1'])
    PC2_mean = np.mean(sdata['PC2'])
    cov = np.cov(sdata['PC1'], sdata['PC2'])
    ax2.scatter(PC1_mean, PC2_mean, color=colors.get(group), s=10*len(sdata['PC1']), label=group, edgecolors=None,
                linewidth=0)

ax2.set_xlim(xlim[0], xlim[1])
ax2.set_ylim(ylim[0], ylim[1])
ax2.set_xlabel('PC1')
ax2.set_ylabel('PC2')
plt.show()

# save figure
fig2.savefig('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported'
             '\PCA_Procrustes\PCA_scatter_MeanRegionLocations_forPaper.pdf', transparent=True)


"""
Procrustes analysis
"""
# run procrustes
stand_latlong, oriented_pcs, disparity_of_data = spatial.procrustes(data1=finalDf[['Longitude', 'Latitude']],
                                                                    data2=finalDf[['PC1', 'PC2']])
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

with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported\PCA_Procrustes'
          '\PCA_Procrustes_Output.txt', 'wb') as output_file:
    output_file.write('Explained Variance for PC1 and PC2: ' + str(pca.explained_variance_ratio_) + '\r')
    output_file.write('Disparity of Data: ' + str(disparity_of_data) + '\r')
    output_file.write('p-value for n=' + str(n) + ': ' + str(p))
output_file.close()
