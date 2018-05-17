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

for sv in data_for_wrs.columns[3:]:
    e = data_for_wrs.loc[data_for_wrs['Region'] == 'east', sv]
    w = data_for_wrs.loc[data_for_wrs['Region'] == 'west', sv]
    s = data_for_wrs.loc[data_for_wrs['Region'] == 'south', sv]
#     print(sv)
#     print('east vs west', ranksums(e, w))
#     print('west vs south', ranksums(w, s))
#     print('south vs east', ranksums(s, e))
#     print('\n')
#     print(sv)
#     ax = sns.violinplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]], inner='stick')
#     ax = sns.set_style('white')
    fig = plt.figure(figsize=(7, 11))
    sns.set(style='white')
    ax = sns.boxplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]], color='None', fliersize=0, width=0.5,
                     linewidth=3)
    ax = sns.stripplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]],
                       palette=['#f17300', '#1f78b4', '#33a02c'],
                       size=7, jitter=True, lw=1)
    #different colors:
    # ax = sns.stripplot(x='Region', y=sv, data=data_for_wrs[['Region', sv]],
    #                    palette=sns.xkcd_palette(['windows blue', 'amber', 'green']), size=7, jitter=True, lw=1)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    # # Calculate number of obs per group & median to position labels
    # medians = data_for_wrs.groupby(['Region'], sort=False)[sv].median().values
    # nobs = data_for_wrs.groupby(['Region'], sort=False).size().values
    # nobs = [str(x) for x in nobs.tolist()]
    # nobs = ["n: " + i for i in nobs]
    #
    # # Add it to the plot
    # pos = range(len(nobs))
    # for tick, label in zip(pos, ax.get_xticklabels()):
    #     plt.text(pos[tick] - 0.25, medians[tick] + 0.4, nobs[tick], horizontalalignment='center', fontsize=14,
    #              color='k', weight='semibold')

    # remove border around plot
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # # adjust ticks
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    #
    # # axis limits
    # plt.ylim(data_for_wrs[sv].min(), data_for_wrs[sv].max())

    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    # ax.set_title(sv, fontsize=30, y=1.05)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.tick_params(labelsize=40)
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=3)

    # # add bar, *, and p-value if significant (.001 = 0.05/(16*3))
    # if ranksums(e, w)[1] < .001:
    #     x1, x2 = 1, 2  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    #     # print(data_for_wrs[sv].max)
    #     y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
    #                 .02 * data_for_wrs[sv].max(), 'k'
    #     plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
    #     plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
    #              fontsize=60, weight='semibold')
    #     plt.text((x1 + x2) * .5 + .7, y + h, 'p=%.2E' % ranksums(e, w)[1], ha='center', va='bottom', color=col,
    #              fontsize=44)
    #
    # if ranksums(s, e)[1] < .001:
    #     x1, x2 = 0, 1  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    #     y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
    #                 .02 * data_for_wrs[sv].max(), 'k'
    #     plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
    #     plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
    #     plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, e)[1], ha='center', va='bottom', color=col,
    #              fontsize=44)
    #
    # if ranksums(s, w)[1] < .001:
    #     x1, x2 = 0, 2  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    #     y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
    #                 .02 * data_for_wrs[sv].max(), 'k'
    #     plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
    #     plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
    #     plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, w)[1], ha='center', va='bottom', color=col,
    #              fontsize=44)

    # add bar, *, and NO p-value if significant (.001 = 0.05/(16*3))
    if ranksums(e, w)[1] < .001:
        if ranksums(e, w)[1] > 1e-07:
            x1, x2 = 1.1, 1.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            # print(data_for_wrs[sv].max)
            y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "*", ha='center', va='bottom', color=col,
                     fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 + .7, y + h, 'p=%.2E' % ranksums(e, w)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)
        else:
            x1, x2 = 1.1, 1.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            # print(data_for_wrs[sv].max)
            y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "**", ha='center', va='bottom', color=col,
                     fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 + .7, y + h, 'p=%.2E' % ranksums(e, w)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)


    if ranksums(s, e)[1] < .001:
        if ranksums(s, e)[1] > 1e-07:
            x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, e)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)
        else:
            x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            y, h, col = data_for_wrs[sv].max() + .05 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "**", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, e)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)

    if ranksums(s, w)[1] < .001:
        if ranksums(s, w)[1] > 1e-07:
            x1, x2 = 0.1, 1.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            y, h, col = data_for_wrs[sv].max() + .15 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, w)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)
        else:
            x1, x2 = 0.1, 1.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
            y, h, col = data_for_wrs[sv].max() + .15 * data_for_wrs[sv].max(), \
                        .02 * data_for_wrs[sv].max(), 'k'
            plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
            plt.text((x1 + x2) * .5, y + h/2, "**", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
            # plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, w)[1], ha='center', va='bottom', color=col,
            #          fontsize=44)

    # plt.tight_layout()
    # pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots_Norm"
    #                "/JunePosterVersion/" + sv + '.pdf')
    # pdf.savefig(orientation='landsccape')
    # pdf.close()

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots_Norm"
                "/JunePosterVersion/" + sv + '.png',
                type='png', dpi=fig.dpi, bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close()

    # plt.show()



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

# code to chop off either end of a cmap
# https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
#
# def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
#     new_cmap = colors.LinearSegmentedColormap.from_list(
#         'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
#         cmap(np.linspace(minval, maxval, n)))
#     return new_cmap
#
# arr = np.linspace(0, 50, 100).reshape((10, 10))
# fig, ax = plt.subplots(ncols=2)
#
# cmap = plt.get_cmap('YlOrBr')
# new_cmap = truncate_colormap(cmap, 0.2, 1)
# ax[0].imshow(arr, interpolation='nearest', cmap=cmap)
# ax[1].imshow(arr, interpolation='nearest', cmap=new_cmap)
# plt.show()


# my_dpi = 96
# fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)
#
# # make the background map
# m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
# m.drawcoastlines()
# m.drawcountries(color='gray')
# m.drawmapboundary(fill_color='white', color='none')
#
# m.hexbin(data_for_heatmaps['Longitude'], data_for_heatmaps['Latitude'], mincnt=1, gridsize=50, cmap='jet')
# m.colorbar()
# plt.show()


"""
Downsampling of data to check we get the same results - only one random sample from each lat/long
"""
# pd.set_option("display.max_rows", 500)
# # print(data_for_wrs.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True))
#
# # # just checking my work
# # print(data_for_wrs.shape)
# # print(data_for_wrs.duplicated(subset=('Latitude', 'Longitude')).sum())
# # print(data_for_wrs.groupby(['Latitude', 'Longitude'], as_index=False).size())
# # print(len(data_for_wrs.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True)))
#
# data_for_wrs_rounded = data_for_wrs.round({'Latitude': 3, 'Longitude': 3})
# data_downsampled = data_for_wrs_rounded.groupby(['Latitude', 'Longitude']).apply(lambda x: x.sample(1)).reset_index(drop=True)
# # print(data_downsampled)
#
# # # plot the new geographical spread of subset of data
# # my_dpi = 96
# # fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)
# #
# # m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
# # m.drawcoastlines()
# # m.drawcountries(color='gray')
# # m.drawmapboundary(fill_color='white', color='none')
# #
# # m.hexbin(data_downsampled['Longitude'], data_downsampled['Latitude'], mincnt=1, gridsize=50, cmap='jet')
# # m.colorbar()
# # plt.show()
#
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






