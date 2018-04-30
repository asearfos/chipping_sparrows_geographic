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
Load data and organize/subset for correlations between 16 song variables and latitude, longitude, and year
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingMonth', 'RecordingTime']
data_for_corr = log_song_data_unique.drop(col_to_skip, axis=1)



"""
Continuous Stats Test on 16 chosen song variables
"""
# spearman_results = subset_corrTable_norm.corr(method='spearman')
# print(spearman_results)
#
# unique_spearman_results = spearman_results.copy().drop(['Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear'], axis=0).drop(
#     spearman_results.columns[4:], axis=1)
#
# print(unique_spearman_results)

def corrfunc(x, y, **kws):
    r, p_r = stats.pearsonr(x, y)
    rho, p_rho = stats.spearmanr(x, y)
    ax = plt.gca()
    ax.annotate("r = {:.2f}, p = {:.2f}\nrho = {:.2f}, p = {:.2f}".format(r, p_r, rho, p_rho),
                xy=(.1, .9), xycoords=ax.transAxes)

# plotting correlations
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/sixteenSongVar_corr_wReg.pdf")
# sns.set(style='white')
# g = sns.pairplot(data=data_for_corr,
#              x_vars=data_for_corr.columns[0:3],
#              y_vars=data_for_corr.columns[4:],
#              kind='reg')
# g.map(corrfunc)
# pdf.savefig()
# pdf.close()
# plt.show()