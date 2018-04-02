import pymysql as sql
import os
import csv
from datetime import datetime
import time
import re

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()


"""
add all the analysis output for FinalDataCompiled for Chippies project to a sql table Chippies_FinalData_AnalysisOutput
"""
analysis_output = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                  "\FinalDataCompilation_AnalysisOutput_20180311_T202015.csv"

with open(analysis_output) as csv_file:
    csv_data = csv.reader(csv_file)
    next(csv_data, None)
    for row in csv_data:
        row = [None if len(x) == 0 else x for x in row]
        row[0] = row[0].replace('SegSyllsOutput_', '').replace('.gzip', '')
        cursor.execute("INSERT INTO asearfos.Chippies_FinalData_AnlaysisOutput"
                       "(`FileName`, `AvgNoteDuration_ms`, "
                       "`AvgNotesFreqModulation_Hz`,"
                       " `AvgNotesLowerFreq_Hz`, `AvgNotesUpperFreq_Hz`, "
                       "`AvgSilenceDuration_ms`, `AvgSyllableDuration_ms`, `AvgSyllsFreqModulation_Hz`, "
                       "`AvgSyllsLowerFreq_Hz`, `AvgSyllsUpperFreq_Hz`, `BoutDuration_ms`, `LargestNoteDuration_ms`, "
                       "`LargestNotesFreqModulation_Hz`, `LargestSilenceDuration_ms`, `LargestSyllableDuration_ms`, "
                       "`LargestSyllsFreqModulation_Hz`, `MaxNotesFreq_Hz`, `MaxSyllsFreq_Hz`, `MeanSyllableStereotypy`, "
                       "`MinNotesFreq_Hz`, `MinSyllsFreq_Hz`, `NoteSizeThreshold`, `NumNotes`, `NumNotesPerSyll`, "
                       "`NumSyllablePerBoutDuration`, `NumSyllables`, `NumSyllablesPerNumUnique`, `NumUniqueSyllables`, "
                       "`OverallNotesFreqRange_Hz`, `OverallSyllsFreqRange_Hz`, `SequentialRepetition`, "
                       "`SmallestNoteDuration_ms`, `SmallestNotesFreqModulation_ms`, `SmallestSilenceDuration_ms`, "
                       "`SmallestSyllableDuration_ms`, `SmallestSyllsFreqModulation_Hz`, `StdNoteDuration_ms`, "
                       "`StdNotesFreqModulation_Hz`, `StdSilenceDuration_ms`, `StdSyllableDuration_ms`, "
                       "`StdSyllableStereotypy`, `StdSyllsFreqModulation_Hz`, `SyllCorrelationThreshold`, "
                       "`SyllablePattern`, `SyllableStereotypy`) "
                       "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                       "%s);", row)

conn.commit()

"""
update catalog numbers by using the filenames
"""

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = LEFT(FileName,locate('_b',FileName)-1) "
               "where chippies.FileName like '%\_b%';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = LEFT(FileName,locate('_44k',FileName)-1) "
               "where chippies.FileName like '%\_44k%';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = LEFT(FileName,locate(' s1',FileName)-1) "
               "where chippies.FileName like '%\ s1%';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = LEFT(FileName,locate(' bout',FileName)-1) "
               "where chippies.FileName like '%\ bout%' and CatalogNo is Null;")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = LEFT(FileName,locate('_',FileName)-1) "
               "where chippies.CatalogNo is Null;")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = '132220' "
               "where chippies.FileName = 'b1s chipping sparrow 132220_b1of1';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput as chippies "
               "set chippies.CatalogNo = '33843' "
               "where chippies.FileName = '33843 bout_b17of31';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput "
               "set	CatalogNo = '9209' "
               "where FileName like '%9209.1%';")

cursor.execute("update asearfos.Chippies_FinalData_AnlaysisOutput "
               "set	CatalogNo = 'Boston12' "
               "where FileName like '%Boston12b%';")

conn.commit()


