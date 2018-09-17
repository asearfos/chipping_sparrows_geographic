import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
import datetime


fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()

"""
Check if song variables are log normal
- had to test some of this in matlab because python's JB function doesn't have the correction for small sample sizes
"""

# # query sql table and make dataframe
# query = "select * from asearfos.Chippies_FinalData_AnalysisOutput " \
#          "where ComparedStatus = 'unique' or ComparedStatus = 'use';"
#
# songVarTable = pd.read_sql(query, conn).drop(['Chippies_FinalData_AnalysisOutput', 'NoteSizeThreshold',
#                                               'SyllCorrelationThreshold'], axis=1)

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
Create table of variables we will be using - only 16
"""

items = "`ChippingSparrows_FinalDataCompilation`.`CatalogNo`," \
        "`ChippingSparrows_FinalDataCompilation`.`FromDatabase`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`ComparedStatus`," \
        "`ChippingSparrows_FinalDataCompilation`.`Latitude`," \
        "`ChippingSparrows_FinalDataCompilation`.`Longitude`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingDay`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingMonth`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingYear`," \
        "`ChippingSparrows_FinalDataCompilation`.`RecordingTime`," \
        "`ChippingSparrows_FinalDataCompilation`.`Region`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgNoteDuration_ms`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgNotesFreqModulation_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgNotesLowerFreq_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgNotesUpperFreq_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgSilenceDuration_ms`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgSyllableDuration_ms`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgSyllsFreqModulation_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgSyllsLowerFreq_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`AvgSyllsUpperFreq_Hz`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`BoutDuration_ms`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`MeanSyllableStereotypy`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`NumNotesPerSyll`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`NumSyllablePerBoutDuration`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`NumSyllables`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`StdNoteDuration_ms`," \
        "`Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported`.`StdNotesFreqModulation_Hz`" \

query2 = ("SELECT %s " \
         "FROM asearfos.Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported " \
         "inner join asearfos.ChippingSparrows_FinalDataCompilation on " \
         "asearfos.Chippies_FinalData_AnalysisOutput_withReChipperedAndReExported.CatalogNo = " \
         "asearfos.ChippingSparrows_FinalDataCompilation.CatalogNo " \
         "where Latitude is not null;" % items)

corrTable = pd.read_sql(query2, conn, parse_dates=False)
corrTable['RecordingTime'] = pd.to_datetime(corrTable['RecordingTime']).dt.time
corrTable['Region'].fillna('mid', inplace=True)

save_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz.csv'
corrTable.to_csv(save_path, sep=',', header=True, index=False)

# log transform (natural log) unless log transform made the data more skewed (JB test - see normality spreadsheet in
# google docs)
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'Latitude', 'Longitude', 'RecordingDay', 'RecordingMonth',
               'RecordingYear', 'RecordingTime', 'Region', 'MeanSyllableStereotypy', 'StdNotesFreqModulation_Hz']

corrTable_norm = corrTable.copy()
for var in corrTable_norm.columns:
        if var not in col_to_skip:
                corrTable_norm[var] = corrTable_norm[var].apply(np.log)

save_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
corrTable_norm.to_csv(save_path, sep=',', header=True, index=False)




