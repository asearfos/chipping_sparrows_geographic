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
import numpy as np
import time
from matplotlib.ticker import FuncFormatter
import csv


"""
Load data and organize/subset for correlations between 16 song variables and latitude, longitude
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)

col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay',
               'RecordingMonth', 'RecordingTime', 'RecordingYear']
data_for_corr = log_song_data_unique.drop(col_to_skip, axis=1)

"""
Continuous Stats Test on 16 chosen song variables
"""

def corrfunc(x, y, **kws):
    rho, p_rho = stats.spearmanr(x, y, nan_policy='omit')
    ax = plt.gca()
    if p_rho < (0.05/(16*2)):
        weight = 'bold'
    else:
        weight = 'normal'

    try:
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, 1.01),
                    xycoords=ax.transAxes,
                    fontsize=8,
                    fontweight=weight)
    except ValueError:
        p_rho = float(ma.getdata(p_rho))
        ax.annotate("rho = {:.2f}, p = {:.2e}".format(rho, p_rho),
                    xy=(.1, 1.01),
                    xycoords=ax.transAxes,
                    fontsize=8,
                    fontweight=weight)

#plotting correlations
pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
               "\StatsOfFinalData_withReChipperReExported"
               "/AnimalBehaviourRevisions/SupplementalCorr"
               "/sixteenSongVar_corr_wReg_onlyLatitude.pdf")
sns.set(style='ticks',
        rc={"font.style": "normal",
            'lines.markersize': 2,
            'axes.labelsize': 5,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8,
            })

# sns.axes_style({'axes.spines.right': True, 'axes.spines.top': True})

g = sns.pairplot(data=data_for_corr,
             x_vars=data_for_corr.columns[0],  # change for latitude or longitude
             y_vars=data_for_corr.columns[3:],
             kind='reg', grid_kws={'despine': False})

# for ax in g.axes.flat:
#     _ = plt.setp(ax.get_yticklabels(), visible=True)`
#     _ = plt.setp(ax.get_xticklabels(), visible=True)

g.map(corrfunc)
pdf.savefig(transparent=True)
pdf.close()
# plt.show()

# make table of results
print(data_for_corr.columns[0], data_for_corr.columns[1])
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject'
          '/StatsOfFinalData_withReChipperReExported'
          '/AnimalBehaviourRevisions/SupplementalCorr'
          '/SongVar_corr_LatLong.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'Lat rho', 'Lat p-value',
                         'Long rho', 'Long p-value'])

    for song_var in data_for_corr.columns[3:]:
        lat_rho, lat_p = stats.spearmanr(data_for_corr['Latitude'],
                                         data_for_corr[song_var],
                                         nan_policy='omit')
        long_rho, long_p = stats.spearmanr(data_for_corr['Longitude'],
                                           data_for_corr[song_var],
                                           nan_policy='omit')

        filewriter.writerow([song_var, lat_rho, lat_p, long_rho, long_p])

"""
Table of results for downsampling
"""

# load in list of random seeds
seed_list = np.genfromtxt('C:/Users/abiga\Box '
                          'Sync\Abigail_Nicole\ChippiesProject'
                          '\FinalDataCompilation\RandomSeeds.csv',
                          delimiter=',', dtype='int')

data_for_corr_rounded = data_for_corr.round({'Latitude': 2, 'Longitude': 2})

spearmanr_lat_p = pd.DataFrame(index=range(1000),
                               columns=[data_for_corr_rounded.columns[3:]])
spearmanr_long_p = pd.DataFrame(index=range(1000),
                                columns=[data_for_corr_rounded.columns[3:]])

for r, seed in zip(range(1000), seed_list):
    sample = data_for_corr_rounded.groupby(['Latitude', 'Longitude']).apply(
        lambda x: x.sample(1, random_state=seed)).reset_index(drop=True)

    for song_var in sample.columns[3:]:
        spearmanr_lat_p.iloc[r][song_var] = stats.spearmanr(
            sample['Latitude'], sample[song_var], nan_policy='omit')[1]
        spearmanr_long_p.iloc[r][song_var] = stats.spearmanr(
            sample['Longitude'], sample[song_var], nan_policy='omit')[1]

downsampling_results = pd.concat([spearmanr_lat_p.max(axis=0),
                                  spearmanr_lat_p.min(axis=0),
                                  spearmanr_long_p.max(axis=0),
                                  spearmanr_long_p.min(axis=0)],
                                 axis=1,
                                 keys=['lat_p_max', 'lat_p_min',
                                       'long_p_max', 'long_p_min'])

downsampling_results.to_csv('C:/Users/abiga/Box '
                            'Sync/Abigail_Nicole/ChippiesProject'
                            '/StatsOfFinalData_withReChipperReExported'
                            '/AnimalBehaviourRevisions/SupplementalCorr'
                            '/SongVar_corr_LatLong_downsampled.csv')


"""
Main figure plots (did not use, just put table of correlations in the main text)
"""

song_variables = ['Mean Note Duration',
                  'Mean Note Frequency Modulation',
                  'Mean Note Frequency Trough',
                  'Mean Note Frequency Peak',
                  'Mean Inter-Syllable Silence Duration',
                  'Mean Syllable Duration',
                  'Mean Syllable Frequency Modulation',
                  'Mean Syllable Frequency Trough',
                  'Mean Syllable Frequency Peak',
                  'Duration of Song Bout',
                  'Mean Stereotypy of Repeated Syllables',
                  'Number of Notes per Syllable',
                  'Syllable Rate',
                  'Total Number of Syllables',
                  'Standard Deviation of Note Duration',
                  'Standard Deviation of Note Frequency Modulation']

log_var = {7: 'ms', 8: 'ms', 16: 'number'}
log_convert_var = {9: 'kHz', 11: 'kHz', 12: 'seconds'}

# take e^x for y-axis
for key, value in log_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white',
            rc={"font.style": "normal",
                'axes.labelsize': 20,
                'xtick.labelsize': 18,
                'ytick.labelsize': 18,
                })
    sns.set_style('ticks')

    ax = sns.regplot(data=data_for_corr,
                     x='Longitude',  # change for latitude or longitude
                     y=data_for_corr.columns[key])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')')
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "\AnimalBehaviourRevisions/SupplementalCorr"
                "/" + data_for_corr.columns[key] + '_noLogAxis_largerFont' + '.pdf',
                type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()


# take e^x for each variable and also convert from Hz to kHz or ms to seconds
for key, value in log_convert_var.items():
    fig = plt.figure(figsize=(7, 11))
    my_dpi = 96
    sns.set(style='white',
            rc={"font.style": "normal",
                'axes.labelsize': 20,
                'xtick.labelsize': 18,
                'ytick.labelsize': 18,
                })
    sns.set_style('ticks')

    ax = sns.regplot(data=data_for_corr,
                     x='Longitude',  # change for latitude or longitude
                     y=data_for_corr.columns[key])

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    ax.set_ylabel(song_variables[key-3] + ' (' + value + ')')
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))


    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "\AnimalBehaviourRevisions/SupplementalCorr"
                "/" + data_for_corr.columns[key] + '_noLogAxis_largerFont' + '.pdf',
                type='pdf', dpi=fig.dpi,
                bbox_inches='tight', transparent=True)
    # plt.cla()
    # plt.clf()
    plt.close()

    # plt.show()