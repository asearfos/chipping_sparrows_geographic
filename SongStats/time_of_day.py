import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy.stats import ranksums
import datetime

"""
Load data and organize/subset for PCA and procrustes testing
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/FinalDataframe_CombinedTables_LogTransformed.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
    drop=True)
col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingMonth', 'RecordingYear', 'Region']
data_for_tod = log_song_data_unique.drop(col_to_skip, axis=1)
data_for_tod['RecordingTime'] = pd.to_datetime(data_for_tod['RecordingTime']).dt.time


"""
Wilcoxon Rank sums for dawn vs day (rough time estimates) 
"""
# # WILCOXON RANKSUMS
# dawn_dur = data_for_tod[data_for_tod['RecordingTime'].le(datetime.time(hour=5, minute=30))]['BoutDuration_ms']
# day_dur = data_for_tod[data_for_tod['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['BoutDuration_ms']
# print('dawn vs day', ranksums(dawn_dur, day_dur))
# print(type(dawn_dur))
#
# # make dataframe with categories dawn and day
# dawn_day_df = pd.DataFrame(columns=('BoutDuration_ms', 'NumSyllables', 'RecordingTime', 'DawnVsDay'))
# dawn_day_df['DawnVsDay'] = dawn_day_df.DawnVsDay.astype(str)
# dawn_day_df[['BoutDuration_ms', 'NumSyllables', 'RecordingTime']] = data_for_tod[['BoutDuration_ms', 'NumSyllables',
#                                                                                   'RecordingTime']]
#
# dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] < (datetime.time(hour=5, minute=30))] = 'Dawn'
# dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] > (datetime.time(hour=8, minute=00))] = 'Day'
#
#
# # FIGURE 1: bout duration between dawn vs. day
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
# ax.set_ylabel('ln(Bout Duration) (ln(ms))', fontsize=50)
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
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + 'DawnVsDay_BoutDuration_Norm' +
#             '.png',
#             type='png', dpi=fig.dpi, bbox_inches='tight')
#
#
# # FIGURE 2: Number of syllables between dawn vs. day
# fig = plt.figure(figsize=(9, 11))
# sns.set(style='white')
# ax = sns.boxplot(x='DawnVsDay', y='NumSyllables', data=dawn_day_df, color='None', fliersize=0, )
# ax = sns.stripplot(x='DawnVsDay', y='NumSyllables', data=dawn_day_df, palette=sns.xkcd_palette(['amber',
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
# ax.set_ylabel('ln(NumSyllables)', fontsize=50)
# ax.set_xlabel('')
# ax.tick_params(labelsize=40)
#
# # add bar if significant
# if ranksums(dawn_dur, day_dur)[1] < .001:
#     x1, x2 = 0, 1  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#     # print(subset_corrTable_wRegion_norm[sv].max)
#     y, h, col = dawn_day_df['NumSyllables'].max() + .05 * dawn_day_df['NumSyllables'].max(), \
#                 .02 * dawn_day_df['NumSyllables'].max(), 'k'
#     plt.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
#     plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
#              fontsize=60, weight='semibold')
#     plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
#              fontsize=44)
#
# # plt.show()
# plt.tight_layout()
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + 'DawnVsDay_NumSyllables_Norm' +
#             '.png',
#             type='png', dpi=fig.dpi, bbox_inches='tight')


"""
Wilcoxon Rank sums for dawn vs day (get actual dawn times for lat/long/date/time) 
"""
from astral import Location
import pandas as pd
from datetime import datetime
import pytz as pz
from tzwhere import tzwhere




print(data_for_tod.head())

tz = tzwhere.tzwhere()

for row in data_for_tod.iterrows():
    print(row['Latitude'], row['Longitude'])
    quit()
    naive_time = datetime.strptime(row.DATE + ' ' + str(row.STARTTIME),
                                   '%Y-%m-%d %H:%M:%S')
    local_tz = pz.timezone(tz.tzNameAt(latitude=row['Latitude'],
                                       longitude=row['Longitude']))
    local_dt = local_tz.localize(naive_time, is_dst=None) # I am forcing non-dst, might need to check this!
    l = Location()
    l.latitude = row['Latitude']
    l.longitude = row['Longitude']
    l.timezone = str(local_dt.tzinfo)
    dawn = l.dawn(date=local_dt)
    time_diff = local_dt - dawn
    # if time_diff.seconds > 86400/2: # If more than 1/2 day after dawn, subtract a day
    #     return time_diff.seconds - 86400
    # return time_diff.seconds

#
# def dawn_offset(row):
#     # Function to calculate for each row DAWN
#     try:
#         naive_time = datetime.strptime(row.DATE + ' ' + str(row.STARTTIME),
#                                        '%Y-%m-%d %H:%M:%S')
#         local_tz = pz.timezone(tz.tzNameAt(latitude=row.LATITUDE,
#                                            longitude=row.LONGITUDE))
#         local_dt = local_tz.localize(naive_time, is_dst=None) # I am forcing non-dst, might need to check this!
#         l = Location()
#         l.latitude = row.LATITUDE
#         l.longitude = row.LONGITUDE
#         l.timezone = str(local_dt.tzinfo)
#         dawn = l.dawn(date=local_dt)
#         time_diff = local_dt - dawn
#         if time_diff.seconds > 86400/2: # If more than 1/2 day after dawn, subtract a day
#             return time_diff.seconds - 86400
#         return time_diff.seconds
#     except:
#         pass
#
#
#
