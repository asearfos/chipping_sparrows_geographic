import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from ifdvsonogramonly import ifdvsonogramonly
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


"""
Load data song data
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
col_to_skip = ['ComparedStatus', 'FromDatabase', 'RecordingDay', 'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# use only east, west and south data
data_ews = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)


"""
Finding an example of East, West, South songs (the ones closes to the average for specified song features of interest)
"""
var_of_interest = ['NumSyllables', 'AvgSyllableDuration_ms', 'AvgSilenceDuration_ms', 'BoutDuration_ms']
var_diffs = ['DiffNumSylls', 'DiffSyllDur', 'DiffSilenceDur', 'DiffBoutDur']

example_files = {}

for region in ['east', 'west', 'south']:
    mean_df = pd.DataFrame(columns=['CatalogNo',
                                    'DiffNumSylls',
                                    'DiffSyllDur',
                                    'DiffSilenceDur',
                                    'DiffBoutDur'])
    for i in range(0, 4):
        region_data = data_ews.loc[data_ews['Region'] == region]
        mean_df['CatalogNo'] = region_data['CatalogNo']
        mean_df[var_diffs[i]] = abs(region_data[var_of_interest[i]] -
                                    region_data[var_of_interest[i]].mean())
    mean_df['DiffSum'] = mean_df[var_diffs].sum(axis=1)
    example_files.update({region: mean_df.loc[mean_df['DiffSum'].idxmin()]['CatalogNo']})
    del mean_df

print(example_files)


"""
Load in example songs and make figures
"""

song_names = ['527118_44k_b1of1-3.wav',
              '72202241_b3of23-3.wav',
              'XC313467_b4of9-3.wav']
for name in song_names:
    song_file = "C:/Users/abiga\Box " \
                "Sync\Abigail_Nicole\ChippiesProject" \
                "\StatsOfFinalData_withReChipperReExported" \
                "\AnimalBehaviourRevisions\ExampleSongsByRegion/" +\
                name
    song, rate = sf.read(song_file)
    sonogram, timeAxis_conversion, freqAxis_conversion = ifdvsonogramonly(song,
                                                                          rate,
                                                                          1024,
                                                                          1010.0,
                                                                          2.0)
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    # sns.set(style='white')
    [rows, cols] = np.shape(sonogram)
    im = plt.imshow(np.log(sonogram+3),
                    cmap='gray_r',
                    extent=[0, cols, 0, rows],
                    aspect='auto')

    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(
            lambda x, p: "%.2f" % (x*timeAxis_conversion/1000)))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(
            lambda x, p: "%.0f" % (x*freqAxis_conversion/1000)))
    plt.tick_params(labelsize=14)
    plt.savefig("C:/Users/abiga\Box "
                "Sync\Abigail_Nicole\ChippiesProject"
                "\StatsOfFinalData_withReChipperReExported"
                "\AnimalBehaviourRevisions\ExampleSongsByRegion/" +
                name + '_sonogram' + '.pdf', type='pdf',
                dpi=fig.dpi, bbox_inches='tight',
                transparent=True)
    # plt.show()
