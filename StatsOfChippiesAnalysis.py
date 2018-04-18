import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy import stats
import datetime


fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()

"""
Check if song variables are log normal
"""

# query sql table and make dataframe
query = "select * from asearfos.Chippies_FinalData_AnlaysisOutput " \
         "where ComparedStatus = 'unique' or ComparedStatus = 'use';"

songVarTable = pd.read_sql(query, conn).drop(['Chippies_FinalData_AnalysisOutput', 'NoteSizeThreshold',
                                              'SyllCorrelationThreshold'], axis=1)

# # songVarTable.to_csv("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject/dataframeToTest")
#
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/SongVariables_histograms.pdf")
# for var in songVarTable.columns:
#     if songVarTable[var].dtype == 'float64' or songVarTable[var].dtype == 'int64':
#         fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
#         fig.suptitle(var + " and Log Normalized", fontsize=16)
#         # plt.figure()
#         a = sns.distplot(songVarTable[var].dropna(), bins=100, kde=False, ax=ax1)
#         a.set_xlabel("jarque_bera: " +
#                     str(stats.jarque_bera(songVarTable[var].dropna())), fontsize=6)
#         b = sns.distplot(songVarTable[var].apply(np.log).dropna(), bins=100, kde=False, ax=ax2)
#         b.set_xlabel("jarque_bera: " +
#                     str(stats.jarque_bera(songVarTable[var].apply(np.log).dropna())), fontsize=6)
#         pdf.savefig()
#         plt.close()
# pdf.close()
#
#

"""
PCA analysis to see which song variable explain most of the variance
"""
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# get only the song variables that are numerical numbers
for var in songVarTable.columns:
        if songVarTable[var].dtype != 'float64' and songVarTable[var].dtype != 'int64':
                songVarTable = songVarTable.drop([var], axis=1)

# drop StdSyllableStereotypy because it is mostly NA
# print(songVarTable.isnull().sum())
songVarTable = songVarTable.drop(['StdSyllableStereotypy'], axis=1)

col_to_skip = ['MeanSyllableStereotypy', 'SequentialRepetition', 'SmallestSyllsFreqModulation_Hz',
               'StdNotesFreqModulation_Hz']

songVarTable_norm = songVarTable.copy()
for var in songVarTable.columns:
        if var not in col_to_skip:
                songVarTable_norm[var] = songVarTable_norm[var].apply(np.log)

# songVarTable_forPCA = StandardScaler().fit_transform(songVarTable_norm)
# # choosing number of components
# pca = PCA()
# PCs = pca.fit_transform(songVarTable_forPCA)
# plt.plot(np.cumsum(pca.explained_variance_ratio_))
# plt.xlabel('number of components')
# plt.ylabel('cumulative explained variance')
# plt.show()
# print(np.shape(PCs))
#
# pca = PCA(n_components=10)
# PCs = pca.fit_transform(songVarTable_forPCA)
# principalDf = pd.DataFrame(data=PCs, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
# print(principalDf.columns)
# print(principalDf.shape)
# print(pca.explained_variance_ratio_)


"""
Autocorrelation of Song Variables
"""
# use log normalized graphs to hopefully be closer to normal distributions
# there is debate as to whether normal distribution is necessary for Pearson's r:
# https://stats.stackexchange.com/questions/3730/pearsons-or-spearmans-correlation-with-non-normal-data
# print(songVarTable_norm.isnull().sum())
# corr_SongVar = songVarTable_norm.corr(method='pearson')
#
# for col in corr_SongVar.columns:
#     for ind in corr_SongVar.index:
#         if 1 > corr_SongVar[col][ind] > 0.8:
#             print(col + ', ' + ind + ', ' + str(corr_SongVar[col][ind]))


"""
Spearman's rho stats for song variables and time, breading season, dawn vs day, space
"""
items = "`ChippingSparrows_FinalDataCompilation`.`Latitude`," \
        "`ChippingSparrows_FinalDataCompilation`.`Longitude`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingMonth`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingYear`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingTime`," \
        "`ChippingSparrows_FinalDataCompilation`.`Region`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgNoteDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgNotesFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgNotesLowerFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgNotesUpperFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgSilenceDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgSyllableDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgSyllsFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgSyllsLowerFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`AvgSyllsUpperFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`BoutDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`LargestNoteDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`LargestNotesFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`LargestSilenceDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`LargestSyllableDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`LargestSyllsFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`MaxNotesFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`MaxSyllsFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`MeanSyllableStereotypy`," \
        "`Chippies_FinalData_AnlaysisOutput`.`MinNotesFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`MinSyllsFreq_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumNotes`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumNotesPerSyll`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumSyllablePerBoutDuration`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumSyllables`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumSyllablesPerNumUnique`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumUniqueSyllables`," \
        "`Chippies_FinalData_AnlaysisOutput`.`OverallNotesFreqRange_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`OverallSyllsFreqRange_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SequentialRepetition`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SmallestNoteDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SmallestNotesFreqModulation_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SmallestSilenceDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SmallestSyllableDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`SmallestSyllsFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdNoteDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdNotesFreqModulation_Hz`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdSilenceDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdSyllableDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdSyllsFreqModulation_Hz`" \

query2 = ("SELECT %s " \
         "FROM asearfos.Chippies_FinalData_AnlaysisOutput " \
         "inner join asearfos.ChippingSparrows_FinalDataCompilation on " \
         "asearfos.Chippies_FinalData_AnlaysisOutput.CatalogNo = " \
         "asearfos.ChippingSparrows_FinalDataCompilation.CatalogNo " \
         "where ComparedStatus = 'use' or ComparedStatus = 'unique';" % items)


corrTable = pd.read_sql(query2, conn).drop(['RecordingTime', 'Region'], axis=1)
corrTable_wRegion = pd.read_sql(query2, conn).drop(['RecordingTime'], axis=1)
corrTable_wTime = pd.read_sql(query2, conn, parse_dates=False).drop(['Region'], axis=1)
corrTable_wTime['RecordingTime'] = pd.to_datetime(corrTable_wTime['RecordingTime']).dt.time


col_to_skip2 = ['Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear',
                'MeanSyllableStereotypy', 'SequentialRepetition', 'SmallestSyllsFreqModulation_Hz',
                'StdNotesFreqModulation_Hz']

corrTable_norm = corrTable.copy()
for var in corrTable_norm.columns:
        if var not in col_to_skip2:
                corrTable_norm[var] = corrTable_norm[var].apply(np.log)

# recordingVars = corrTable_norm.columns[0:5]
# songVars = corrTable_norm.columns[5:]

# gg = sns.pairplot(data=corrTable_norm,
#                   y_vars=songVars[0:4],
#                   x_vars=recordingVars,)
# plt.show()

"""
16 chosen song variables
"""
subset_corrTable_norm = corrTable_norm.copy()
toss_list = ['LargestNoteDuration_ms', 'LargestNotesFreqModulation_Hz', 'LargestSilenceDuration_ms',
             'LargestSyllableDuration_ms', 'LargestSyllsFreqModulation_Hz', 'MaxNotesFreq_Hz', 'MaxSyllsFreq_Hz',
             'MinNotesFreq_Hz', 'MinSyllsFreq_Hz', 'NumNotes', 'NumSyllablesPerNumUnique', 'NumUniqueSyllables',
             'OverallNotesFreqRange_Hz', 'OverallSyllsFreqRange_Hz', 'SequentialRepetition',
             'SmallestNoteDuration_ms', 'SmallestNotesFreqModulation_ms', 'SmallestSilenceDuration_ms',
             'SmallestSyllableDuration_ms', 'SmallestSyllsFreqModulation_Hz', 'StdSilenceDuration_ms',
             'StdSyllableDuration_ms', 'StdSyllsFreqModulation_Hz']
subset_corrTable_norm = subset_corrTable_norm.drop(toss_list, axis=1)


"""
Continuous Stats Test on 16 chosen song variables
"""
spearman_results = subset_corrTable_norm.corr(method='spearman')
# print(spearman_results)

unique_spearman_results = spearman_results.copy().drop(['Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear'], axis=0).drop(
    spearman_results.columns[4:], axis=1)

# print(unique_spearman_results)

# plotting correlations
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/sixteenSongVar_corr.pdf")
# sns.pairplot(data=subset_corrTable_norm,
#              y_vars=subset_corrTable_norm.columns[5:],
#              x_vars=subset_corrTable_norm.columns[1:5],)
# pdf.savefig()
# plt.close()
# pdf.close()

"""
Discrete Stats Tests using Regions
"""
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import ranksums

col_to_skip3 = ['Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear', 'Region',
                'MeanSyllableStereotypy', 'SequentialRepetition', 'SmallestSyllsFreqModulation_Hz',
                'StdNotesFreqModulation_Hz']

corrTable_wRegion_norm = corrTable_wRegion.copy()
for var in corrTable_wRegion_norm.columns:
        if var not in col_to_skip3:
                corrTable_wRegion_norm[var] = corrTable_wRegion_norm[var].apply(np.log)

subset_corrTable_wRegion_norm = corrTable_wRegion_norm.copy()
toss_list3 = ['Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear', 'LargestNoteDuration_ms',
             'LargestNotesFreqModulation_Hz',
             'LargestSilenceDuration_ms',
             'LargestSyllableDuration_ms', 'LargestSyllsFreqModulation_Hz', 'MaxNotesFreq_Hz', 'MaxSyllsFreq_Hz',
             'MinNotesFreq_Hz', 'MinSyllsFreq_Hz', 'NumNotes', 'NumSyllablesPerNumUnique', 'NumUniqueSyllables',
             'OverallNotesFreqRange_Hz', 'OverallSyllsFreqRange_Hz', 'SequentialRepetition',
             'SmallestNoteDuration_ms', 'SmallestNotesFreqModulation_ms', 'SmallestSilenceDuration_ms',
             'SmallestSyllableDuration_ms', 'SmallestSyllsFreqModulation_Hz', 'StdSilenceDuration_ms',
             'StdSyllableDuration_ms', 'StdSyllsFreqModulation_Hz']
subset_corrTable_wRegion_norm = subset_corrTable_wRegion_norm.drop(toss_list3, axis=1)

# print(subset_corrTable_wRegion_norm)

# print(subset_corrTable_wRegion_norm[['AvgNoteDuration_ms', 'Region']])
# for sv in subset_corrTable_wRegion_norm.columns[1:]:
#     string = "'" + sv + " ~ C(Region)'"
#     print(string)
#     # mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
#     # print(sm.stats.anova_lm(mod, typ=2))

# RUN ANOVAS FOR EACH SONG VARIABLE AND REGION
# string = 'AvgNoteDuration_ms ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgNotesFreqModulation_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgNotesLowerFreq_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgNotesUpperFreq_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgSilenceDuration_ms ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgSyllableDuration_ms ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgSyllsFreqModulation_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgSyllsLowerFreq_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'AvgSyllsUpperFreq_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'BoutDuration_ms ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'MeanSyllableStereotypy ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'NumNotesPerSyll ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'NumSyllablePerBoutDuration ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'NumSyllables ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'StdNoteDuration_ms ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))
#
# string = 'StdNotesFreqModulation_Hz ~ C(Region)'
# mod = ols(string, data=subset_corrTable_wRegion_norm).fit() #Specify C for Categorical
# print(string)
# print(sm.stats.anova_lm(mod, typ=2))


# WILCOXON RANKSUMS
# for regions: east, west, south and the 16 variables

# for sv in subset_corrTable_wRegion_norm.columns[1:]:
#     e = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'east', sv]
#     w = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'west', sv]
#     s = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'south', sv]
# #     print(sv)
# #     print('east vs west', ranksums(e, w))
# #     print('west vs south', ranksums(w, s))
# #     print('south vs east', ranksums(s, e))
# #     print('\n')
# #     print(sv)
# #     ax = sns.violinplot(x='Region', y=sv, data=subset_corrTable_wRegion_norm[['Region', sv]], inner='stick')
# #     ax = sns.set_style('white')
#     fig = plt.figure(figsize=(9, 11))
#     sns.set(style='white')
#     ax = sns.boxplot(x='Region', y=sv, data=subset_corrTable_wRegion_norm[['Region', sv]], color='None', fliersize=0)
#     ax = sns.stripplot(x='Region', y=sv, data=subset_corrTable_wRegion_norm[['Region', sv]],
#                        palette=sns.xkcd_palette(['windows blue', 'amber', 'green']), size=7, jitter=True, lw=1)
#
#     # Make the boxplot fully transparent
#     for patch in ax.artists:
#         r, g, b, a = patch.get_facecolor()
#         patch.set_facecolor((r, g, b, 0))
#
#     # # Calculate number of obs per group & median to position labels
#     # medians = subset_corrTable_wRegion_norm.groupby(['Region'], sort=False)[sv].median().values
#     # nobs = subset_corrTable_wRegion_norm.groupby(['Region'], sort=False).size().values
#     # nobs = [str(x) for x in nobs.tolist()]
#     # nobs = ["n: " + i for i in nobs]
#     #
#     # # Add it to the plot
#     # pos = range(len(nobs))
#     # for tick, label in zip(pos, ax.get_xticklabels()):
#     #     plt.text(pos[tick] - 0.25, medians[tick] + 0.4, nobs[tick], horizontalalignment='center', fontsize=14,
#     #              color='k', weight='semibold')
#
#     # remove border around plot
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#
#     # # adjust ticks
#     # plt.yticks(fontsize=14)
#     # plt.xticks(fontsize=14)
#     #
#     # # axis limits
#     # plt.ylim(subset_corrTable_wRegion_norm[sv].min(), subset_corrTable_wRegion_norm[sv].max())
#
#     ax.yaxis.set_ticks_position('left')
#     ax.xaxis.set_ticks_position('bottom')
#     # ax.set_title(sv, fontsize=30, y=1.05)
#     ax.set_ylabel('')
#     ax.set_xlabel('')
#     ax.tick_params(labelsize=40)
#     ax.set(xticklabels=[])
#
#     # add bar if significant
#     if ranksums(e, w)[1] < .001:
#         x1, x2 = 1, 2  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#         # print(subset_corrTable_wRegion_norm[sv].max)
#         y, h, col = subset_corrTable_wRegion_norm[sv].max() + .05 * subset_corrTable_wRegion_norm[sv].max(), \
#                     .02 * subset_corrTable_wRegion_norm[sv].max(), 'k'
#         plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
#         plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
#                  fontsize=60, weight='semibold')
#         plt.text((x1 + x2) * .5 + .7, y + h, 'p=%.2E' % ranksums(e, w)[1], ha='center', va='bottom', color=col,
#                  fontsize=44)
#
#     if ranksums(s, e)[1] < .001:
#         x1, x2 = 0, 1  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#         y, h, col = subset_corrTable_wRegion_norm[sv].max() + .05 * subset_corrTable_wRegion_norm[sv].max(), \
#                     .02 * subset_corrTable_wRegion_norm[sv].max(), 'k'
#         plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
#         plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
#         plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, e)[1], ha='center', va='bottom', color=col,
#                  fontsize=44)
#
#     if ranksums(s, w)[1] < .001:
#         x1, x2 = 0, 2  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#         y, h, col = subset_corrTable_wRegion_norm[sv].max() + .05 * subset_corrTable_wRegion_norm[sv].max(), \
#                     .02 * subset_corrTable_wRegion_norm[sv].max(), 'k'
#         plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
#         plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col, fontsize=60, weight='semibold')
#         plt.text((x1 + x2) * .5 - .7, y + h, 'p=%.2E' % ranksums(s, w)[1], ha='center', va='bottom', color=col,
#                  fontsize=44)
#     # pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots/" + sv + '.pdf')
#     # plt.tight_layout()
#     # pdf.savefig(orientation='landsccape')
#     # pdf.close()
#
#     # manager = plt.get_current_fig_manager()
#     # manager.window.showMaximized()
#
#     plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/BoxPlots_Norm/" + sv + '.png',
#                 type='png', dpi=fig.dpi, bbox_inches='tight')
#
#
#     # plt.show()
#     plt.cla()
#     plt.clf()
#     plt.close()

""""
Get a random representative from each region
"""

e_numSylls = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'east', 'NumSyllables']
w_numSylls = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'west', 'NumSyllables']
s_numSylls = subset_corrTable_wRegion_norm.loc[subset_corrTable_wRegion_norm['Region'] == 'south', 'NumSyllables']

# get song from each region with ~median number of syllables


"""
Wilcoxon Ranksums for dawn vs day 
"""
# WILCOXON RANKSUMS
# for dawn vs. day for length of bout *******Note these are not normalized*******
# dawn_times = corrTable_wTime[corrTable_wTime['RecordingTime'].le(datetime.time(hour=5, minute=30))]['RecordingTime']
# day_times = corrTable_wTime[corrTable_wTime['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['RecordingTime']

# dawn_dur = corrTable_wTime[corrTable_wTime['RecordingTime'].le(datetime.time(hour=5, minute=30))]['BoutDuration_ms']
# day_dur = corrTable_wTime[corrTable_wTime['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['BoutDuration_ms']
# print('dawn vs day', ranksums(dawn_dur, day_dur))
# print(type(dawn_dur))
#
# # make dataframe with categories dawn and day
# dawn_day_df = pd.DataFrame(columns=('BoutDuration_ms', 'RecordingTime', 'DawnVsDay'))
# dawn_day_df['DawnVsDay'] = dawn_day_df.DawnVsDay.astype(str)
# dawn_day_df[['BoutDuration_ms', 'RecordingTime']] = corrTable_wTime[['BoutDuration_ms', 'RecordingTime']]
#
# dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] < (datetime.time(hour=5, minute=30))] = 'Dawn'
# dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] > (datetime.time(hour=8, minute=00))] = 'Day'
#
# fig = plt.figure(figsize=(9, 11))
# sns.set(style='white')
# ax = sns.boxplot(x='DawnVsDay', y='BoutDuration_ms', data=dawn_day_df, color='None', fliersize=0, )
# ax = sns.stripplot(x='DawnVsDay', y='BoutDuration_ms', data=dawn_day_df, palette=sns.xkcd_palette(['amber',
#                          'green']), size=7, jitter=True, lw=1)
#
# # Make the boxplot fully transparent
# for patch in ax.artists:
#     r, g, b, a = patch.get_facecolor()
#     patch.set_facecolor((r, g, b, 0))
#
# # remove border around plot
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
#
# ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_ticks_position('bottom')
# # ax.set_title('Dawn Vs Day', fontsize=30, y=1.05)
# ax.set_ylabel('Bout Duration (ms)', fontsize=50)
# ax.set_xlabel('')
# ax.tick_params(labelsize=40)
#
# # add bar if significant
# if ranksums(dawn_dur, day_dur)[1] < .001:
#     x1, x2 = 0, 1  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#     # print(subset_corrTable_wRegion_norm[sv].max)
#     y, h, col = dawn_day_df['BoutDuration_ms'].max() + .05 * dawn_day_df['BoutDuration_ms'].max(), \
#                 .02 * dawn_day_df['BoutDuration_ms'].max(), 'k'
#     plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
#     plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
#              fontsize=60, weight='semibold')
#     plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
#              fontsize=44)
#
# # plt.show()
# plt.tight_layout()
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + 'DawnVsDay' +
#             '.png',
#             type='png', dpi=fig.dpi, bbox_inches='tight')

## doesn't work yet
# TOD_duration = corrTable_wTime[['RecordingTime', 'BoutDuration_ms']]
# print(TOD_duration)
# TOD_duration.plot('RecordingTime', 'BoutDuration_ms', style='.')
# # sns.lmplot('RecordingTime', 'BoutDuration_ms', data=TOD_duration)
# # plt.scatter(corrTable_wTime.timestamp(corrTable_wTime['RecordingTime'])['RecordingTime'], corrTable_wTime[
# #     'BoutDuration_ms'])
# plt.gcf().autofmt_xdate()
# plt.show()

""""
HEAT MAPS OF SIGNIFICANT FEATURES ON GEOGRAPHICAL MAP
"""
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable

# for songChar in subset_corrTable_wRegion_norm.columns[1:]:
# # for songChar in ['NumSyllables']:
#
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
#     # print(subset_corrTable_wRegion_norm[songChar])
#     # print(corrTable_norm[songChar])
#     n = m.scatter(corrTable_norm['Longitude'], corrTable_norm['Latitude'], s=100, alpha=0.6, c=corrTable_norm[songChar],
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

