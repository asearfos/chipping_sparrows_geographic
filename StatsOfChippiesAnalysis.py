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
                corrTable_norm[var] = corrTable_norm[var].apply(np.log)

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
#     print(sv)
#     print('east vs west', ranksums(e, w))
#     print('west vs south', ranksums(w, s))
#     print('south vs east', ranksums(s, e))
#     print('\n')

"""
Wilcoxon Ranksums for dawn vs day 
"""
# # WILCOXON RANKSUMS
# # for dawn vs. day for length of bout
# dawn_times = corrTable_wTime[corrTable_wTime['RecordingTime'].le(datetime.time(hour=6, minute=0))]['RecordingTime']
# day_times = corrTable_wTime[corrTable_wTime['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['RecordingTime']
#
# dawn_dur = corrTable_wTime[corrTable_wTime['RecordingTime'].le(datetime.time(hour=5, minute=30))]['BoutDuration_ms']
# day_dur = corrTable_wTime[corrTable_wTime['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['BoutDuration_ms']
# print('dawn vs day', ranksums(dawn_dur, day_dur))


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

# set the dimension of the figure
# my_dpi = 96
# plt.figure(figsize=(2600/my_dpi, 1800/my_dpi), dpi=my_dpi)

# make the background map
m = Basemap(llcrnrlat=0, llcrnrlon=-179, urcrnrlat=76, urcrnrlon=-44)
m.drawcoastlines()
m.drawcountries(color='gray')
m.drawmapboundary(fill_color='white')

songChar = 'AvgNoteDuration_ms'
n = m.scatter(corrTable_norm['Longitude'], corrTable_norm['Latitude'], alpha=0.4, c=corrTable_norm[songChar],
          cmap='seismic', edgecolor='black', lw='1')

plt.colorbar(pad=0.004)
# plt.suptitle(songChar)

# print(plt.get_backend())
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
plt.show()

# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + songChar + '.pdf')
#
# pdf.savefig()
# pdf.close()


#
# n = Basemap(width=12000000, height=9000000, projection='lcc',
#             resolution='c', lat_1=45., lat_2=55, lat_0=50, lon_0=-107.)
# n.drawcoastlines()
# plt.show()
#
