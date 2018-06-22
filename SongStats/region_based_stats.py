import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import ranksums
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors
import csv

"""
Load data and organize/subset wilcoxon rank sums test and heatmaps overlayed on geographical maps 
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# use only east, west and south data for wilcoxon rank sums
data_for_wrs = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)

# use all unique/use data, do not remove any mid region data, for heatmaps
data_for_heatmaps = data_subset.copy()


"""
Discrete Stats Tests using Regions:
Wilcoxon Rank sums for regions: east, west, south and the 16 song variables
"""
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData/BoxPlots_Norm/PaperVersion'
          '/region_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable', 'EW Wilcoxon p', 'EW p-value', 'ES Wilcoxon p', 'ES p-value', 'WS Wilcoxon p',
                         'WS p-value'])

    # song_variables = ['Mean Note Duration (log(ms))',
    #                   'Mean Note Frequency Modulation (log(Hz))',
    #                   'Mean Note Frequency Trough (log(Hz))',
    #                   'Mean Note Frequency Peak (log(Hz))',
    #                   'Mean Inter-Syllable Silence Duration (log(ms))',
    #                   'Mean Syllable Duration (log(ms))',
    #                   'Mean Syllable Frequency Modulation (log(Hz))',
    #                   'Mean Syllable Frequency Trough (log(Hz))',
    #                   'Mean Syllable Frequency Peak (log(Hz))',
    #                   'Duration of Song Bout (log(ms))',
    #                   'Mean Stereotypy of Repeated Syllables (%)',
    #                   'Number of Notes per Syllable',
    #                   'Syllable Rate (log(number/ms))',
    #                   'Total Number of Syllables',
    #                   'Standard Deviation of Note Duration (log(ms))',
    #                   'Standard Deviation of Note Frequency Modulation (Hz)']

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

    song_units = ['log(ms)',
                      'log(Hz)',
                      'log(Hz)',
                      'log(Hz)',
                      'log(ms)',
                      'log(ms)',
                      'log(Hz)',
                      'log(Hz)',
                      'log(Hz)',
                      'log(ms)',
                      '(%)',
                      'Number',
                      'log(number/ms)',
                      'Number',
                      'log(ms)',
                      'Hz']

    count = 0
    for sv in data_for_wrs.columns[3:]:
        e = data_for_wrs.loc[data_for_wrs['Region'] == 'east', sv]
        w = data_for_wrs.loc[data_for_wrs['Region'] == 'west', sv]
        s = data_for_wrs.loc[data_for_wrs['Region'] == 'south', sv]

        filewriter.writerow([sv, ranksums(e, w)[0], ranksums(e, w)[1], ranksums(e, s)[0], ranksums(e, s)[1],
                             ranksums(w, s)[0], ranksums(w, s)[1]])

        fig = plt.figure(figsize=(7, 11))
        sns.set(style='white')
        ax = sns.boxplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]], color='None', fliersize=0, width=0.5,
                         linewidth=2)
        ax = sns.stripplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]],
                           palette=['#f17300', '#1f78b4', '#33a02c'],
                           size=7, jitter=True, lw=1, alpha=0.6)
        #different colors:
        # ax = sns.stripplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]],
        #                    palette=sns.xkcd_palette(['windows blue', 'amber', 'green']), size=7, jitter=True, lw=1)

        # Make the boxplot fully transparent
        for patch in ax.artists:
            r, g, b, a = patch.get_facecolor()
            patch.set_facecolor((r, g, b, 0))

        # remove border around plot
        # ax.spines["top"].set_visible(False)7
        # ax.spines["right"].set_visible(False)

        # # adjust ticks
        # plt.yticks(fontsize=14)
        # plt.xticks(fontsize=14)
        #
        # # axis limits
        # plt.ylim(data_for_wrs[sv].min(), data_for_wrs[sv].max())

        ax.set_title(song_variables[count], fontsize=25, y=1.05)
        ax.set_ylabel(song_units[count], fontsize=20)
        ax.set_xlabel('')
        ax.tick_params(labelsize=15, direction='out')
        ax.set(xticklabels=[])
        plt.setp(ax.spines.values(), linewidth=2)
        count += 1

        plt.tight_layout()
        pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots_Norm"
                       "/PaperVersion/" + sv + '.pdf')
        pdf.savefig(orientation='landsccape')
        pdf.close()

        # manager = plt.get_current_fig_manager()
        # manager.window.showMaximized()
        #
        # plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots_Norm"
        #             "/PaperVersion/" + sv + '.png',
        #             type='png', dpi=fig.dpi, bbox_inches='tight')
        # plt.cla()
        # plt.clf()
        # plt.close()

        # plt.show()

quit()

""""
HEAT MAPS OF SIGNIFICANT FEATURES ON GEOGRAPHICAL MAP
"""
#
# for songChar in data_for_heatmaps.columns[3:]:
#     # plt.close('all')
#
#     # Set the dimension of the figure
#     my_dpi = 96
#     fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)
#
#     # make the background map
#     m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
#     m.drawcoastlines()
#     m.drawcountries(color='gray')
#     m.drawmapboundary(fill_color='white', color='none')
#
#     # songChar = 'AvgNoteDuration_ms'
#     # print(data_for_wrs[songChar])
#     # print(corrTable_norm[songChar])
#     n = m.scatter(data_for_heatmaps['Longitude'], data_for_heatmaps['Latitude'], s=100, alpha=0.6, c=data_for_heatmaps[songChar],
#               cmap='seismic', edgecolor='black', lw='0.5')
#
#
#     divider = make_axes_locatable(plt.gca())
#     cax = divider.append_axes("right", "2%", pad="1%")
#     cbar = plt.colorbar(n, cax=cax)
#     cbar.ax.tick_params(labelsize=40)
#
#     plt.tight_layout()
#     #
#     # pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + songChar + '.pdf')
#     #
#     # pdf.savefig(dpi=fig.dpi, orientation='landsccape')
#     # pdf.close()
#
#     plt.show()
#     # plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/GeoPlots/" + songChar + '.png',
#     #             type='png', dpi=fig.dpi, bbox_inches='tight')
#


""""
Binned heatmap showing geographical distribution of data
"""
#
# # plot locations of all the song data collected --> this includes for all regions the unique songs and all songs
# # chosen as use for possible duplicates
#
# my_dpi = 96
# fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi, frameon=False)
#
# # make the background map
# m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
# m.drawcoastlines(color='k', linewidth=1.5)
# m.drawcountries(color='k', linewidth=1.5)
# m.drawstates(color='gray')
# m.drawmapboundary(fill_color='w', color='none')
#
# m.hexbin(data_for_heatmaps['Longitude'], data_for_heatmaps['Latitude'], mincnt=1, gridsize=50, cmap='cool')
# cb = m.colorbar()
# cb.ax.tick_params(labelsize=25)
# plt.tight_layout()
#
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\GeoSpreadOfRecordings/" +
#                'AllRecordingLocations_UniqueUse' + '.pdf')
#
# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()
#
# # plt.show()
#
# # plot locations of song data used for computations--> this includes all unique songs and all songs chosen as use for
# # possible duplicates but only for East and West and South (excludes mid)
# my_dpi = 96
# fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi, frameon=False)
#
# # make the background map
# m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
# m.drawcoastlines(color='k', linewidth=1.5)
# m.drawcountries(color='k', linewidth=1.5)
# m.drawstates(color='gray')
# m.drawmapboundary(fill_color='w', color='none')
#
# m.hexbin(data_for_wrs['Longitude'], data_for_wrs['Latitude'], mincnt=1, gridsize=50, cmap='cool')
# cb = m.colorbar()
# cb.ax.tick_params(labelsize=25)
# plt.tight_layout()
#
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\GeoSpreadOfRecordings/" +
#                'EastWestSouthRecordingLocations_UniqueUse' + '.pdf')
#
# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()
#
# # plt.show()

"""
Downsampling of data to check we get the same results - only one random sample from each lat/long
"""
pd.set_option("display.max_rows", 500)
# print(data_for_wrs.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True))

# # just checking my work
# print(data_for_wrs.shape)
# print(data_for_wrs.duplicated(subset=('Latitude', 'Longitude')).sum())
# print(data_for_wrs.groupby(['Latitude', 'Longitude'], as_index=False).size())
# print(len(data_for_wrs.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True)))

# round to the third decimal place
data_for_wrs_rounded = data_for_wrs.round({'Latitude': 3, 'Longitude': 3})
data_downsampled = data_for_wrs_rounded.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True)
# print(data_downsampled)

# # plot the new geographical spread of subset of data
# my_dpi = 96
# fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)
#
# m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
# m.drawcoastlines(color='k', linewidth=1.5)
# m.drawcountries(color='k', linewidth=1.5)
# m.drawstates(color='gray')
# m.drawmapboundary(fill_color='w', color='none')
#
# m.hexbin(data_downsampled['Longitude'], data_downsampled['Latitude'], mincnt=1, gridsize=50, cmap='cool')
# cb = m.colorbar()
# cb.ax.tick_params(labelsize=25)
# plt.tight_layout()
#
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\GeoSpreadOfRecordings/" +
#                'EastWestSouthRecordingLocations_UniqueUse_binned' + '.pdf')
#
# pdf.savefig(dpi=fig.dpi, orientation='landscape')
# pdf.close()
#
# # plt.show()

# ranksums_EW = pd.DataFrame(index=range(1000), columns=[data_for_wrs_rounded.columns[3:]])
# ranksums_ES = pd.DataFrame(index=range(1000), columns=[data_for_wrs_rounded.columns[3:]])
# ranksums_WS = pd.DataFrame(index=range(1000), columns=[data_for_wrs_rounded.columns[3:]])
# for r in range(1000):
#     sample = data_for_wrs_rounded.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True)
#
#     for sv in sample.columns[3:]:
#         e = sample.loc[sample['Region'] == 'east', sv]
#         w = sample.loc[sample['Region'] == 'west', sv]
#         s = sample.loc[sample['Region'] == 'south', sv]
#
#         ranksums_EW.iloc[r][sv] = ranksums(e, w)[1]
#         ranksums_ES.iloc[r][sv] = ranksums(e, s)[1]
#         ranksums_WS.iloc[r][sv] = ranksums(w, s)[1]
#
# # print(ranksums_EW)
# print('EW: max\n', ranksums_EW.max(axis=0))
# print('EW: min\n', ranksums_EW.min(axis=0))
# print('ES: max\n', ranksums_ES.max(axis=0))
# print('ES: min\n', ranksums_ES.min(axis=0))
# print('WS: max\n', ranksums_WS.max(axis=0))
# print('WS: min\n', ranksums_WS.min(axis=0))






