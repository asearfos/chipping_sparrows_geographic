import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy.stats import ranksums
import csv
from matplotlib.ticker import FuncFormatter


"""
Load data and organize/subset wilcoxon rank sums test 
"""
# load in song data
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

col_to_skip = ['FromDatabase', 'Latitude', 'Longitude', 'RecordingDay', 'RecordingMonth', 'RecordingYear',
               'RecordingTime']
data_subset = log_song_data.drop(col_to_skip, axis=1)

# load in time data --> before or after sunrise, twilights, and noon (only going to use sunrise and noon)
data_path = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported\TimeAnalysis" \
            "\FinalData_LogTransformed_relativeToSunriseTwilightsNoon.csv"
time_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)
# must remove duplicates -- have more than one bird from same recording -- duplicate catalog number and time data
time_data = time_data.drop_duplicates()

# combine tables using catalog no
combined_df = pd.merge(data_subset, time_data, on='CatalogNo')

# only keep unique and use and ones with time data
combined_df_unique = combined_df.loc[combined_df['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
combined_df_unique = combined_df_unique.drop(combined_df_unique[combined_df_unique.Sunrise ==
                                                                '--'].index).copy().reset_index(drop=True)

"""
Wilcoxon Ranksums
"""

with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported/TimeAnalysis'
          '/SunriseCivilTwilightNoon_WilcoxonRanksums.csv', 'wb') as file:
    filewriter = csv.writer(file, delimiter=',')
    filewriter.writerow(['Song Variable',
                         'Before After Sunrise p-value',
                         'Before Sunrise and After Noon p-value',
                         'After Sunrise and After Noon p-value',
                         'Before After Civil Twilight p-value',
                         'Before Civil Twilight and After Noon p-value',
                         'After Civil Twilight and After Noon p-value'])

    song_variables = ['Duration of Song Bout (s)',
                      'Total Number of Syllables (number)']

    song_units = ['log(ms)', 'log(number)']

    for sv in ['BoutDuration_ms', 'NumSyllables']:
        before_sunrise = combined_df_unique.loc[combined_df_unique['Sunrise'] == 'before sunrise', sv]
        after_sunrise = combined_df_unique.loc[combined_df_unique['Sunrise'] == 'after sunrise', sv]
        sunrise_after_noon = combined_df_unique.loc[combined_df_unique['Sunrise'] == 'after noon', sv]

        before_civil = combined_df_unique.loc[combined_df_unique['CivilTwilight'] == 'before civil', sv]
        after_civil = combined_df_unique.loc[combined_df_unique['CivilTwilight'] == 'after civil', sv]
        civil_after_noon = combined_df_unique.loc[combined_df_unique['CivilTwilight'] == 'after noon', sv]

        filewriter.writerow([sv, ranksums(before_sunrise, after_sunrise)[1],
                             ranksums(before_sunrise, sunrise_after_noon)[1],
                             ranksums(after_sunrise, sunrise_after_noon)[1],
                             ranksums(before_civil, after_civil)[1],
                             ranksums(before_civil, civil_after_noon)[1],
                             ranksums(after_civil, civil_after_noon)[1]])
""""
Box plots (change out the sv, the index for title, and the formatting for the two different box plot sets - bout 
duration and number of syllables)
"""
# box plot for duration of song bout, take exponential (and convert from ms to s for bout duration)
# for sv in ['BoutDuration_ms']:  # for bout duration
for sv in ['NumSyllables']:  # for num of sylls
    fig = plt.figure(figsize=(7, 11))
    sns.set(style='white')
    ax = sns.boxplot(x='CivilTwilight', y=sv, data=combined_df_unique[['CivilTwilight', sv]], color='None',
                     fliersize=0, width=0.5, linewidth=2, order=['before civil', 'after civil', 'after noon'])
    ax = sns.stripplot(x='CivilTwilight', y=sv, data=combined_df_unique[['CivilTwilight', sv]],
                       order=['before civil', 'after civil', 'after noon'],
                       palette=['black', '#95B2B8', '#F1D302'], size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    # ax.set_ylabel(song_variables[0], fontsize=30)  # for bout duration
    ax.set_ylabel(song_variables[1], fontsize=30)  # for num of sylls
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    # ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))  # for bout duration
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))  # for num of sylls

    # plt.tight_layout()
    # pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/TimeAnalysis"
    #                "/PaperVersion/" + sv + '_Civil' + '.pdf')
    # pdf.savefig(orientation='landscape')
    # pdf.close()

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
                "/TimeAnalysis/" + sv + '_Civil' + '.pdf', type='pdf', dpi=fig.dpi, bbox_inches='tight',
                transparent=True)
    # plt.show()

    fig = plt.figure(figsize=(7, 11))
    sns.set(style='white')
    ax = sns.boxplot(x='Sunrise', y=sv, data=combined_df_unique[['Sunrise', sv]], color='None',
                     fliersize=0, width=0.5, linewidth=2, order=['before sunrise', 'after sunrise', 'after noon'])
    ax = sns.stripplot(x='Sunrise', y=sv, data=combined_df_unique[['Sunrise', sv]],
                       order=['before sunrise', 'after sunrise', 'after noon'],
                       palette=['black', '#95B2B8', '#F1D302'], size=7, jitter=True, lw=1, alpha=0.6)

    # Make the boxplot fully transparent
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0))

    # ax.set_ylabel(song_variables[0], fontsize=30)  # for bout duration
    ax.set_ylabel(song_variables[1], fontsize=30)  # for num of sylls
    ax.set_xlabel('')
    ax.tick_params(labelsize=30, direction='out')
    ax.set(xticklabels=[])
    plt.setp(ax.spines.values(), linewidth=2)
    # ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x)/1000)))  # for bout duration
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "%.1f" % (np.exp(x))))  # for num of sylls

    # plt.tight_layout()
    # pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported/TimeAnalysis"
    #                "/PaperVersion/" + sv + '_Sunrise' + '.pdf')
    # pdf.savefig(orientation='landscape')
    # pdf.close()
    # plt.show()

    plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData_withReChipperReExported"
                "/TimeAnalysis/" + sv + '_Sunrise' + '.pdf', type='pdf', dpi=fig.dpi, bbox_inches='tight',
                transparent=True)
