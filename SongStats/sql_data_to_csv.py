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
# query = "select * from asearfos.Chippies_FinalData_AnlaysisOutput " \
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
        "`Chippies_FinalData_AnlaysisOutput`.`ComparedStatus`," \
        "`ChippingSparrows_FinalDataCompilation`.`Latitude`," \
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
        "`Chippies_FinalData_AnlaysisOutput`.`MeanSyllableStereotypy`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumNotesPerSyll`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumSyllablePerBoutDuration`," \
        "`Chippies_FinalData_AnlaysisOutput`.`NumSyllables`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdNoteDuration_ms`," \
        "`Chippies_FinalData_AnlaysisOutput`.`StdNotesFreqModulation_Hz`" \

query2 = ("SELECT %s " \
         "FROM asearfos.Chippies_FinalData_AnlaysisOutput " \
         "inner join asearfos.ChippingSparrows_FinalDataCompilation on " \
         "asearfos.Chippies_FinalData_AnlaysisOutput.CatalogNo = " \
         "asearfos.ChippingSparrows_FinalDataCompilation.CatalogNo " \
         "where Latitude is not null;" % items)

corrTable = pd.read_sql(query2, conn, parse_dates=False)
corrTable['RecordingTime'] = pd.to_datetime(corrTable['RecordingTime']).dt.time
corrTable['Region'].fillna('mid', inplace=True)

save_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables.csv'
corrTable.to_csv(save_path, sep=',', header=True, index=False)

# log transform (natural log) unless log transform made the data more skewed (JB test - see normality spreadsheet in
# google docs)
col_to_skip = ['CatalogNo', 'ComparedStatus', 'Latitude', 'Longitude', 'RecordingMonth', 'RecordingYear',
                'RecordingTime', 'Region', 'MeanSyllableStereotypy', 'StdNotesFreqModulation_Hz']

corrTable_norm = corrTable.copy()
for var in corrTable_norm.columns:
        if var not in col_to_skip:
                corrTable_norm[var] = corrTable_norm[var].apply(np.log)

save_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
corrTable.to_csv(save_path, sep=',', header=True, index=False)




