import pandas as pd

"""
Load data and organize/subset wilcoxon rank sums test and heatmaps overlayed on geographical maps 
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
col_to_skip = ['ComparedStatus', 'FromDatabase', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# use only east, west and south data
data_ews = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)


"""
Finding an example of East, West, South songs
"""
var_of_interest = ['NumSyllables', 'AvgSyllableDuration_ms', 'AvgSilenceDuration_ms', 'BoutDuration_ms']
var_diffs = ['DiffNumSylls', 'DiffSyllDur', 'DiffSilenceDur', 'DiffBoutDur']

example_files = {}

for region in ['east', 'west', 'south']:
    median = pd.DataFrame(columns=['CatalogNo', 'DiffNumSylls', 'DiffSyllDur', 'DiffSilenceDur', 'DiffBoutDur'])
    for i in range(0, 4):
        region_data = data_ews.loc[data_ews['Region'] == region]
        median['CatalogNo'] = region_data['CatalogNo']
        median[var_diffs[i]] = abs(region_data[var_of_interest[i]] - region_data[var_of_interest[i]].mean())
    median['DiffSum'] = median[var_diffs].sum(axis=1)
    example_files.update({region: median.loc[median['DiffSum'].idxmin()]['CatalogNo']})
    del median

print(example_files)

