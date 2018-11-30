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
Load data and organize/subset for correlations between 16 song variables and latitude, longitude, and year
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay', 'RecordingMonth']
data_for_corr = log_song_data_unique.drop(col_to_skip, axis=1)
data_for_corr['RecordingTime'] = pd.to_datetime(data_for_corr['RecordingTime'])
data_for_corr['RecordingTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in data_for_corr['RecordingTime']]

column_names = ['Latitude', 'Longitude', 'RecordingYear', 'RecordingTime', 'Region',
                'Mean Note Duration (log(ms))',
                'Mean Note Frequency Modulation (log(Hz))',
                'Mean Note Frequency Trough (log(Hz))',
                'Mean Note Frequency Peak (log(Hz))',
                'Mean Inter-Syllable Silence Duration (log(ms))',
                'Mean Syllable Duration (log(ms))',
                'Mean Syllable Frequency Modulation (log(Hz))',
                'Mean Syllable Frequency Trough (log(Hz))',
                'Mean Syllable Frequency Peak (log(Hz))',
                'Duration of Song Bout (log(ms))',
                'Mean Stereotypy of Repeated Syllables (%)',
                'Number of Notes per Syllable (log(number))',
                'Syllable Rate (log(number/ms))',
                'Total Number of Syllables (log(number))',
                'Standard Deviation of Note Duration (log(ms))',
                'Standard Deviation of Note Frequency Modulation (Hz)']

data_for_corr.columns = column_names

"""
Continuous Stats Test on 16 chosen song variables (pearsons and spearmans, only use spearmans for the paper)
"""

def corrfunc(x, y, **kws):
    rho, p_rho = stats.spearmanr(x, y, nan_policy='omit')
    ax = plt.gca()
    if p_rho < (0.05/(16*4)):
        weight = 'bold'
    else:
        weight = 'normal'

    try:
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, 1), xycoords=ax.transAxes, fontsize=8, fontweight=weight)
    except ValueError:
        p_rho = float(ma.getdata(p_rho))
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, 1), xycoords=ax.transAxes, fontsize=8, fontweight=weight)

    if x.name == 'RecordingTime':
        labels = [item.get_text() for item in ax.get_xticklabels()]
        ax.set_xticklabels([time.strftime('%H:%M', time.gmtime(float(label)*100000)) for label in labels])

#plotting correlations
pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SupplementalCorr"
               "/sixteenSongVar_corr_wReg_updated_withTime.pdf")
sns.set(style='white',
        rc={"font.style": "normal",
            'lines.markersize': 2,
            'axes.labelsize': 5,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8})

g = sns.pairplot(data=data_for_corr,
             x_vars=data_for_corr.columns[0:4],
             y_vars=data_for_corr.columns[5:],
             kind='reg')

g.map(corrfunc)
pdf.savefig(transparent=True)
pdf.close()
# plt.show()

# did not use in the paper
"""
Correlation of song variables over year, split into east and west
"""

data_for_corr_ew = data_for_corr.loc[data_for_corr['Region'].isin(['east', 'west'])].copy().reset_index(
    drop=True)

def corrfunc(x, y, **kws):
    ls = {"east": 0.97, "west": .02}
    rho, p_rho = stats.spearmanr(x, y, nan_policy='omit')
    ax = plt.gca()
    if p_rho < (0.05/(16*4)):
        weight = 'bold'
    else:
        weight = 'normal'

    try:
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, ls[kws.get('label', "0")]), xycoords=ax.transAxes, fontsize=8, fontweight=weight,
                    color=kws.get('color', 'g'))
    except ValueError:
        p_rho = float(ma.getdata(p_rho))
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, ls[kws.get('label', "0")]), xycoords=ax.transAxes, fontsize=8, fontweight=weight,
                    color=kws.get('color', 'g'))

# plotting correlations
pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/SupplementalCorr"
               "/sixteenSongVar_corr_wReg_divergingTraits.pdf")
sns.set(style='white',
        rc={"font.style": "normal",
            'lines.markersize': 2,
            'axes.labelsize': 6,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8})
g = sns.pairplot(data=data_for_corr_ew,
             x_vars=data_for_corr_ew.columns[2],
             y_vars=data_for_corr_ew.columns[5:],
             kind='reg', hue='Region', palette=['#1f78b4', '#33a02c'])

g._legend.remove()
g.map(corrfunc)
pdf.savefig(transparent=True)
pdf.close()
# plt.show()
