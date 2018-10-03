import pandas as pd
import numpy as np
import csv

"""
Some files were not exported as 44100Hz and so we had to re-export and re-chipper for accurate measurements.
Here we are updating the FinalDataCompilation_AnalysisOutput with the newly analyzed 44100Hz files (96). Note during
this re-analysis an additional file was tossed so that will need to be removed as well (30432251_b1of12). AMS.
"""

# Load in FinalDataCompilation_AnalysisOutput
FinalData_AnalysisOutput_file = "C:/Users/abiga\Box " \
                                "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                                "\FinalDataCompilation_AnalysisOutput_20180311_T202015.csv"
FinalData_AnalysisOutput_table = pd.read_csv(FinalData_AnalysisOutput_file, header=0, index_col=None, encoding='latin1')
FinalData_AnalysisOutput_table.set_index('FileName', inplace=True)

# load in the new results for the files that were reChippered
reChipper_file = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                 "/reChipper_AnalysisOutput_20180916_T141247.csv"
reChipper_table = pd.read_csv(reChipper_file, header=0, index_col=None, encoding='latin1')
reChipper_table.set_index('FileName', inplace=True)

# Load in the new results for files that were re-exported as 44100Hz
reExported44100Hz_file = "C:/Users/abiga\Box " \
                         "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                         "/reExportedAs44100Hz_AnalysisOutput_20180907_T100552.csv"
reExported44100Hz_table = pd.read_csv(reExported44100Hz_file, header=0, index_col=None, encoding='latin1')
reExported44100Hz_table.set_index('FileName', inplace=True)

# Join the tables using filename
FinalData_AnalysisOutput_table.update(reChipper_table)
FinalData_AnalysisOutput_table.update(reExported44100Hz_table)

# add the file that was tossed previously but is now chippered
newrow = reChipper_table.loc['SegSyllsOutput_Boston26 bout.gzip']
FinalData_AnalysisOutput_table = FinalData_AnalysisOutput_table.append(newrow)

# read in csv of files to toss (after rechipper and non44100 and checking duplicates
toss_file = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation/newTossList_AfterReChipper.csv"
with open(toss_file, 'r') as f:
  reader = csv.reader(f)
  next(reader, None)
  toss_list = list(reader)

# remove the toss list files
for i in range(len(toss_list)):
    FinalData_AnalysisOutput_table.drop(toss_list[i][0], inplace=True)

print(FinalData_AnalysisOutput_table.shape)

# # save as csv (This will need to be used in other scripts to update SQL)
# FinalData_AnalysisOutput_table.to_csv("C:/Users/abiga\Box "
#                                       "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation"
#                                       "\FinalDataCompilation_AnalysisOutput_20180311_T202015_withReChipper_thenWithReExportedAs44100Hz.csv")
#
