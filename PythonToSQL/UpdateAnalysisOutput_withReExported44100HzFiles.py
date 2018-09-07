import pandas as pd
import numpy as np


"""
Some files were not exported as 44100Hz and so we had to re-export and re-chipper for accurate measurements.
Here we are updating the FinalDataCompilation_AnalysisOutput with the newly analyzed 44100Hz files (96). Note during
this re-analysis an additional file was tossed so that will need to be removed as well (30432251_b1of12). AMS.
"""

# Load in FinalDataCompilation_AnalysisOutput
# import juncos datatable
FinalData_AnalysisOutput_file = "C:/Users/abiga\Box " \
                                "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                                "\FinalDataCompilation_AnalysisOutput_20180311_T202015.csv"
FinalData_AnalysisOutput_table = pd.read_csv(FinalData_AnalysisOutput_file, header=0, index_col=None, encoding='latin1')


# Load in the new results for files that were re-exported as 44100Hz
reExported44100Hz_file = "C:/Users/abiga\Box " \
                         "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                         "/reExportedAs44100Hz_AnalysisOutput_20180907_T100552.csv"
reExported44100Hz_table = pd.read_csv(reExported44100Hz_file, header=0, index_col=None, encoding='latin1')

# Join the tables using filename
FinalData_AnalysisOutput_table.update(reExported44100Hz_table)

# remove the newly tossed file
FinalData_AnalysisOutput_table = FinalData_AnalysisOutput_table[FinalData_AnalysisOutput_table.FileName !=
                                                                'SegSyllsOutput_30432251_b1of2.gzip']

# save as csv (This will need to be used in other scripts to update SQL)
FinalData_AnalysisOutput_table.to_csv("C:/Users/abiga\Box " \
                                "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation" \
                                "\FinalDataCompilation_AnalysisOutput_20180311_T202015_withReExportedAs44100Hz.csv")
