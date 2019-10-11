import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from mpl_toolkits.basemap import Basemap

"""
Load data song data
"""
data_path = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation' + \
            '/AnimalBehaviour_SupplementalDataTable2_addedMid.csv'
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

log_song_data_unique = log_song_data.loc[log_song_data[
    'ComparedStatus'].isin(['unique', 'use'])].copy().reset_index(drop=True)
col_to_skip = ['CatalogNo', 'FromDatabase', 'ComparedStatus', 'RecordingDay',
               'RecordingMonth', 'RecordingYear', 'RecordingTime']
data_subset = log_song_data_unique.drop(col_to_skip, axis=1)

# use all unique/use data, do not remove any mid region data, for heatmaps
data_for_heatmaps = data_subset.copy()
data_for_heatmaps_rounded = data_for_heatmaps.round({'Latitude': 2,
                                                     'Longitude': 2})

# use only east, west and south data for wilcoxon rank sums
data_for_wrs = data_subset.drop(data_subset[data_subset.Region == 'mid'].index).copy().reset_index(drop=True)


def convert_lon_lat_points_to_meters_using_transform(points, tran):
    # maybe there is a better way to get long/lat into meters but this works ok
    return np.array([tran(long, lat) for long, lat in points])


""""
Binned heatmap showing geographical distribution of data

Projection used in ArcGIS for Fig 2:
North_America_Lambert_Conformal_Conic
WKID: 102009 Authority: Esri

Projection: Lambert_Conformal_Conic
False_Easting: 0.0
False_Northing: 0.0
Central_Meridian: -96.0
Standard_Parallel_1: 20.0
Standard_Parallel_2: 60.0
Latitude_Of_Origin: 40.0
Linear Unit: Meter (1.0)

Geographic Coordinate System: GCS_North_American_1983
Angular Unit: Degree (0.0174532925199433)
Prime Meridian: Greenwich (0.0)
Datum: D_North_American_1983
  Spheroid: GRS_1980
    Semimajor Axis: 6378137.0
    Semiminor Axis: 6356752.314140356
    Inverse Flattening: 298.257222101
"""



# plot locations of all the song data collected --> this includes for all
# regions the unique songs and all songs chosen as use from possible duplicates

my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi),
                 dpi=my_dpi,
                 frameon=False)

# make the background map
m = Basemap(width=12000000,
            height=9000000,
            rsphere=(6378137.00, 6356752.3142),
            resolution='l',
            area_thresh=10000.,
            projection='lcc',
            lat_1=20.,
            lat_2=60,
            lat_0=40,
            lon_0=-96)
m.drawcoastlines(color='k',
                 linewidth=1.5)
m.drawcountries(color='k',
                linewidth=1.5)
m.drawmapboundary(fill_color='w',
                  color='none')

# get random points in meters
points = convert_lon_lat_points_to_meters_using_transform(
    zip(data_for_heatmaps['Longitude'], data_for_heatmaps['Latitude']), m)

# draw the hexbin
# points[:,i]: selects all rows but just the ith column - used to turn
# list or long,lat pairs into lists of just long and lat but in the same order.
# gridsize: set the number of hexagons in the x and y dimension
# mincnt: set the minimum count in a hexagon for it to be drawn
# cmap: set the colour map to use
m.hexbin(points[:, 0],
         points[:, 1],
         bins='log',
         gridsize=75,
         mincnt=1,
         cmap='cool')

cb = m.colorbar()

ticks_number = []
t_old = []
for t in cb.ax.get_yticklabels():
    t_old.append(float(t.get_text()))
    new_tick = float(t.get_text().replace(t.get_text(), str(round(
        10**float(t.get_text()), 1))))
    ticks_number.append(new_tick)
cb.set_ticks(t_old)
cb.set_ticklabels(["%.2f" % e for e in ticks_number])
cb.ax.tick_params(labelsize=25)
cb.set_label('Number', size=25)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
               "\StatsOfFinalData_withReChipperReExported"
               "/AnimalBehaviourRevisions/GeoSpreadOfRecordings/" +
               'AllRecordingLocations_UniqueUse_logBins_rounded_lambert.pdf')

pdf.savefig(dpi=fig.dpi, orientation='landscape', transparent=True)
pdf.close()

plt.show()

# plot locations of song data used for computations-->
# this includes all unique songs and all songs chosen as use for
# possible duplicates but only for East and West and South (excludes mid)
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi),
                 dpi=my_dpi,
                 frameon=False)

# make the background map
m = Basemap(width=12000000,
            height=9000000,
            rsphere=(6378137.00,6356752.3142),
            resolution='l',
            area_thresh=10000.,
            projection='lcc',
            lat_1=20.,
            lat_2=60,
            lat_0=40,
            lon_0=-96)
m.drawcoastlines(color='k',
                 linewidth=1.5)
m.drawcountries(color='k',
                linewidth=1.5)
m.drawmapboundary(fill_color='w',
                  color='none')

# get random points in meters
points = convert_lon_lat_points_to_meters_using_transform(
    zip(data_for_wrs['Longitude'], data_for_wrs['Latitude']), m)

# draw the hexbin
# points[:,i]: selects all rows but just the ith column - used to turn
# list or long,lat pairs into lists of just long and lat but in the same order.
# gridsize: set the number of hexagons in the x and y dimension
# mincnt: set the minimum count in a hexagon for it to be drawn
# cmap: set the colour map to use
m.hexbin(points[:, 0],
         points[:, 1],
         bins='log',
         gridsize=75,
         mincnt=1,
         cmap='cool')

cb = m.colorbar()

ticks_number = []
t_old = []
for t in cb.ax.get_yticklabels():
    t_old.append(float(t.get_text()))
    new_tick = float(t.get_text().replace(t.get_text(), str(round(
        10**float(t.get_text()), 1))))
    ticks_number.append(new_tick)
cb.set_ticks(t_old)
cb.set_ticklabels(["%.2f" % e for e in ticks_number])
cb.ax.tick_params(labelsize=25)
cb.set_label('Number', size=25)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
               "\StatsOfFinalData_withReChipperReExported"
               "/AnimalBehaviourRevisions/GeoSpreadOfRecordings/" +
               'EastWestSouthRecordingLocations_UniqueUse_logBins_rounded'
               '_lambert.pdf')

pdf.savefig(dpi=fig.dpi, orientation='landscape', transparent=True)
pdf.close()

plt.show()


"""
Plot one example of downsampled dataset - only one random sample from each 
lat/long 
"""

pd.set_option("display.max_rows", 500)

print('data with mid', data_subset.shape)
print('data for wrs', data_for_wrs.shape)
print('data for heatmaps size', data_for_heatmaps.shape)
print('data for heatmaps rounded size', data_for_heatmaps_rounded.shape)
print('number of duplicates', data_for_heatmaps_rounded.duplicated(subset=(
      'Latitude', 'Longitude')).sum())

print(data_for_heatmaps_rounded.groupby(['Latitude', 'Longitude'],
                                        as_index=False).size().sort_values(
    ascending=False))

data_downsampled = data_for_heatmaps_rounded.groupby(
    ['Latitude', 'Longitude']).apply(
    lambda x: x.sample(1, random_state=42)).reset_index(drop=True)

print(data_downsampled.groupby(['Latitude', 'Longitude'],
                               as_index=False).size().sort_values(
        ascending=False))
print('data after downsampled', data_downsampled.shape)

# plot the new geographical spread of subset of data
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi),
                 dpi=my_dpi)

m = Basemap(width=12000000,
            height=9000000,
            rsphere=(6378137.00, 6356752.3142),
            resolution='l',
            area_thresh=10000.,
            projection='lcc',
            lat_1=20.,
            lat_2=60,
            lat_0=40,
            lon_0=-96)
m.drawcoastlines(color='k',
                 linewidth=1.5)
m.drawcountries(color='k',
                linewidth=1.5)
m.drawmapboundary(fill_color='w',
                  color='none')

# get random points in meters
points = convert_lon_lat_points_to_meters_using_transform(
    zip(data_downsampled['Longitude'], data_downsampled['Latitude']), m)

# draw the hexbin
# points[:,i]: selects all rows but just the ith column - used to turn
# list or long,lat pairs into lists of just long and lat but in the same order.
# gridsize: set the number of hexagons in the x and y dimension
# mincnt: set the minimum count in a hexagon for it to be drawn
# cmap: set the colour map to use
m.hexbin(points[:, 0],
         points[:, 1],
         bins='log',
         gridsize=75,
         mincnt=1,
         cmap='cool')

cb = m.colorbar()

ticks_number = []
t_old = []
for t in cb.ax.get_yticklabels():
    t_old.append(float(t.get_text()))
    new_tick = float(t.get_text().replace(t.get_text(), str(round(
        10**float(t.get_text()), 1))))
    ticks_number.append(new_tick)
cb.set_ticks(t_old)
cb.set_ticklabels(["%.2f" % e for e in ticks_number])
cb.ax.tick_params(labelsize=25)
cb.set_label('Number', size=25)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject"
               "\StatsOfFinalData_withReChipperReExported"
               "/AnimalBehaviourRevisions/GeoSpreadOfRecordings/" +
               'AllRecordingLocations_UniqueUse_downsampled_logBins'
               '_rounded_lambert.pdf')

pdf.savefig(dpi=fig.dpi, orientation='landscape', transparent=True)
pdf.close()

plt.show()
