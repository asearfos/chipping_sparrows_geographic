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

# log_song_data_unique = log_song_data.loc[log_song_data['ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(
#     drop=True)
log_song_data_unique = log_song_data.copy()

col_to_skip = ['CatalogNo', 'ComparedStatus', 'RecordingMonth', 'RecordingYear', 'Region']
data_for_tod = log_song_data_unique.copy()
data_for_tod = data_for_tod.drop(col_to_skip, axis=1)
data_for_tod['RecordingTime'] = pd.to_datetime(data_for_tod['RecordingTime']).dt.time

col_to_skip2 = ['CatalogNo', 'ComparedStatus', 'Region']
data_for_dawn = log_song_data_unique.copy()
data_for_dawn = data_for_dawn.drop(col_to_skip2, axis=1)
data_for_dawn['RecordingTime'] = pd.to_datetime(data_for_dawn['RecordingTime']).dt.time

"""
Wilcoxon Rank sums for dawn vs day (rough time estimates) 
"""
# WILCOXON RANKSUMS
dawn_dur = data_for_tod[data_for_tod['RecordingTime'].le(datetime.time(hour=5, minute=30))]['BoutDuration_ms']
day_dur = data_for_tod[data_for_tod['RecordingTime'].ge(datetime.time(hour=8, minute=0))]['BoutDuration_ms']
print('dawn vs day', ranksums(dawn_dur, day_dur))
print(type(dawn_dur))

# make dataframe with categories dawn and day
dawn_day_df = pd.DataFrame(columns=('BoutDuration_ms', 'NumSyllables', 'RecordingTime', 'DawnVsDay'))
dawn_day_df['DawnVsDay'] = dawn_day_df.DawnVsDay.astype(str)
dawn_day_df[['BoutDuration_ms', 'NumSyllables', 'RecordingTime']] = data_for_tod[['BoutDuration_ms', 'NumSyllables',
                                                                                  'RecordingTime']]

dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] < (datetime.time(hour=5, minute=30))] = 'Dawn'
dawn_day_df['DawnVsDay'][dawn_day_df['RecordingTime'] > (datetime.time(hour=8, minute=00))] = 'Day'


# FIGURE 1: bout duration between dawn vs. day
fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x='DawnVsDay', y='BoutDuration_ms', data=dawn_day_df, color='None', fliersize=0, width=0.5,
                 linewidth=3)
ax = sns.stripplot(x='DawnVsDay', y='BoutDuration_ms', data=dawn_day_df, palette=['#1f78b4', '#33a02c'],
                   size=7, jitter=True, lw=1)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

# remove border around plot
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
# ax.set_title('Dawn Vs Day', fontsize=30, y=1.05)
ax.set_ylabel('ln(Bout Duration) (ln(ms))', fontsize=50)
ax.set_xlabel('')
ax.tick_params(labelsize=40)
plt.setp(ax.spines.values(), linewidth=3)


# add bar if significant
if ranksums(dawn_dur, day_dur)[1] < .001:
    if ranksums(dawn_dur, day_dur) > 1e-07:
        x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
        # print(subset_corrTable_wRegion_norm[sv].max)
        y, h, col = dawn_day_df['BoutDuration_ms'].max() + .05 * dawn_day_df['BoutDuration_ms'].max(), \
                    .02 * dawn_day_df['BoutDuration_ms'].max(), 'k'
        plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
        plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
                 fontsize=60, weight='semibold')
        # plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
        #          fontsize=44)
    else:
        x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
        # print(subset_corrTable_wRegion_norm[sv].max)
        y, h, col = dawn_day_df['BoutDuration_ms'].max() + .05 * dawn_day_df['BoutDuration_ms'].max(), \
                    .02 * dawn_day_df['BoutDuration_ms'].max(), 'k'
        plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
        plt.text((x1 + x2) * .5, y + h, "**", ha='center', va='bottom', color=col,
                 fontsize=60, weight='semibold')
        # plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
        #          fontsize=44)

# plt.show()
plt.tight_layout()
plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/TimeAnalysis/JunePosterVersions"
            "/" + 'DawnVsDay_BoutDuration_Norm' + '.png', type='png', dpi=fig.dpi, bbox_inches='tight')


# FIGURE 2: Number of syllables between dawn vs. day
fig = plt.figure(figsize=(7, 11))
sns.set(style='white')
ax = sns.boxplot(x='DawnVsDay', y='NumSyllables', data=dawn_day_df, color='None', fliersize=0, width=0.5, linewidth=3)
ax = sns.stripplot(x='DawnVsDay', y='NumSyllables', data=dawn_day_df, palette=['#1f78b4', '#33a02c'],
                   size=7, jitter=True, lw=1)

# Make the boxplot fully transparent
for patch in ax.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0))

# remove border around plot
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
# ax.set_title('Dawn Vs Day', fontsize=30, y=1.05)
ax.set_ylabel('ln(NumSyllables)', fontsize=50)
ax.set_xlabel('')
ax.tick_params(labelsize=40)
plt.setp(ax.spines.values(), linewidth=3)

# add bar if significant
if ranksums(dawn_dur, day_dur)[1] < .001:
    if ranksums(dawn_dur, day_dur)[1] > 1e-07:
        x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
        # print(subset_corrTable_wRegion_norm[sv].max)
        y, h, col = dawn_day_df['NumSyllables'].max() + .05 * dawn_day_df['NumSyllables'].max(), \
                    .02 * dawn_day_df['NumSyllables'].max(), 'k'
        plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
        plt.text((x1 + x2) * .5, y + h, "*", ha='center', va='bottom', color=col,
                 fontsize=60, weight='semibold')
        # plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
        #          fontsize=44)
    else:
        x1, x2 = 0.1, 0.9  # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
        # print(subset_corrTable_wRegion_norm[sv].max)
        y, h, col = dawn_day_df['NumSyllables'].max() + .05 * dawn_day_df['NumSyllables'].max(), \
                    .02 * dawn_day_df['NumSyllables'].max(), 'k'
        plt.plot([x1, x2], [y + h, y + h], lw=3, c=col)
        plt.text((x1 + x2) * .5, y + h, "**", ha='center', va='bottom', color=col,
                 fontsize=60, weight='semibold')
        # plt.text((x1 + x2) * .5 + .6, y + h, 'p=%.2E' % ranksums(dawn_dur, day_dur)[1], ha='center', va='bottom', color=col,
        #          fontsize=44)

# plt.show()
plt.tight_layout()
plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/TimeAnalysis/JunePosterVersions"
            "/" + 'DawnVsDay_NumSyllables_Norm' + '.png', type='png', dpi=fig.dpi, bbox_inches='tight')


"""
Wilcoxon Rank sums for dawn vs day (get actual dawn times for lat/long/date/time) 
"""
# import astral
# from astral import Location
# import pandas as pd
# from datetime import datetime
# import pytz as pz
# from tzwhere import tzwhere
#
#
# tz = tzwhere.tzwhere()
# relative_times = []
# for row in data_for_dawn.iterrows():
#     if (~np.isnan(row[1]['RecordingYear']) and
#         ~np.isnan(row[1]['RecordingDay']) and
#         str(row[1]['RecordingTime']) != 'nan'):
#
#         # print(row[1]['Latitude'])
#         # print(row[1]['Longitude'])
#         # print(row[1]['RecordingYear'])
#         # print(row[1]['RecordingMonth'])
#         # print(row[1]['RecordingDay'])
#         # print(row[1]['RecordingTime'])
#         naive_time = datetime.strptime(str(int(row[1]['RecordingYear'])) + '-' + str(int(row[1]['RecordingMonth'])) + '-' +
#                                        str(int(row[1]['RecordingDay'])) + ' ' + str(row[1]['RecordingTime']),
#                                        '%Y-%m-%d %H:%M:%S')
#         # print(naive_time)
#         timezone = tz.tzNameAt(latitude=row[1]['Latitude'], longitude=row[1]['Longitude'])
#         # print(timezone)
#         if timezone is not None:
#             local_tz = pz.timezone(timezone)
#             # print(local_tz)
#             local_dt = local_tz.localize(naive_time, is_dst=None) # I am forcing non-dst, might need to check this!
#             # print(local_dt)
#             l = Location()
#             l.latitude = row[1]['Latitude']
#             l.longitude = row[1]['Longitude']
#             l.timezone = str(local_dt.tzinfo)
#             # print(l.timezone)
#
#             try:
#                 sunrise = l.sunrise(date=local_dt)
#                 # print(sunrise)
#                 try:
#                     if sunrise < local_dt:
#                         relative_times.append('after sunrise')
#                     else:
#                         relative_times.append('before sunrise')
#                 except ValueError:
#                     relative_times.append('--')
#             except astral.AstralError:
#                 relative_times.append('--')
#         else:
#             relative_times.append('--')
#     else:
#         relative_times.append('--')
# # print(relative_times)


    # time_diff = local_dt - dawn
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
# """
# Wilcoxon Rank sums for dawn vs day (get actual dawn times for lat/long/date/time)
# """
# import astral
# from astral import Location
# import pandas as pd
# from datetime import datetime
# import pytz as pz
# from tzwhere import tzwhere
# from timezonefinder import TimezoneFinder
#
# tf = TimezoneFinder()
# relative_times = []
# sunrise_times = []
# for row in data_for_dawn.iterrows():
#     if (~np.isnan(row[1]['RecordingYear']) and
#         ~np.isnan(row[1]['RecordingDay']) and
#         str(row[1]['RecordingTime']) != 'nan'):
#
#         # print(row[1]['Latitude'])
#         # print(row[1]['Longitude'])
#         # print(row[1]['RecordingYear'])
#         # print(row[1]['RecordingMonth'])
#         # print(row[1]['RecordingDay'])
#         # print(row[1]['RecordingTime'])
#         naive_time = datetime.strptime(str(int(row[1]['RecordingYear'])) + '-' + str(int(row[1]['RecordingMonth'])) + '-' +
#                                        str(int(row[1]['RecordingDay'])) + ' ' + str(row[1]['RecordingTime']),
#                                        '%Y-%m-%d %H:%M:%S')
#         # print(naive_time)
#         timezone = tf.timezone_at(lng=row[1]['Longitude'], lat=row[1]['Latitude'])
#         # timezone = tz.tzNameAt(latitude=row[1]['Latitude'], longitude=row[1]['Longitude'])
#     # if timezone is not None:
#         local_tz = pz.timezone(timezone)
#         # print(local_tz)
#         local_dt = local_tz.localize(naive_time, is_dst=None) # I am forcing non-dst, might need to check this!
#         # print(local_dt)
#         l = Location()
#         l.latitude = row[1]['Latitude']
#         l.longitude = row[1]['Longitude']
#         l.timezone = str(local_dt.tzinfo)
#         # print(l.timezone)
#
#         try:
#             sunrise = l.dawn(date=local_dt)
#             # print(datetime.time(sunrise))
#             try:
#                 if sunrise < local_dt:
#                     relative_times.append('after civil')
#                     sunrise_times.append(datetime.time(sunrise).strftime("%H:%M:%S"))
#                 else:
#                     relative_times.append('before civil')
#                     sunrise_times.append(datetime.time(sunrise).strftime("%H:%M:%S"))
#             except ValueError:
#                 relative_times.append('--')
#                 sunrise_times.append('--')
#         except astral.AstralError:
#             relative_times.append('--')
#             sunrise_times.append('--')
#     # else:
#     #     print(timezone)
#     #     print(row[1]['Latitude'], row[1]['Longitude'])
#     #     relative_times.append('--')
#     else:
#         relative_times.append('--')
#         sunrise_times.append('--')
# print(relative_times)
# print(sunrise_times)
#
