import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy import stats
import datetime
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable


Haplo_Locations = pd.read_table("C:/Users/abiga\Box "
                                        "Sync\Abigail_Nicole\ChippiesProject\GeneticData\Mila_ControlRegionSeq"
                                        "\Mila_HaplotypeToLocation_correctedCA.txt", delimiter="\t")

Haplo_Locations_wFreq = Haplo_Locations.groupby(['Latitude', 'Longitude']).size().reset_index(name='NumAtLocation')
print(Haplo_Locations_wFreq)

# Set the dimension of the figure
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)

# make the background map
m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
m.drawcoastlines()
m.drawcountries(color='gray')
m.drawmapboundary(fill_color='white', color='none')

# songChar = 'AvgNoteDuration_ms'
# print(subset_corrTable_wRegion_norm[songChar])
# print(corrTable_norm[songChar])
n = m.scatter(Haplo_Locations_wFreq['Longitude'], Haplo_Locations_wFreq['Latitude'], s=200*Haplo_Locations_wFreq[
    'NumAtLocation'], color='k')


# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "2%", pad="1%")
# cbar = plt.colorbar(n, cax=cax)
# cbar.ax.tick_params(labelsize=40)

plt.tight_layout()
#
# pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/" + songChar + '.pdf')
#
# pdf.savefig(dpi=fig.dpi, orientation='landsccape')
# pdf.close()

# plt.show()
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/GeoPlots/" + 'Haplo_Locations_wFreq' + '.png',
#             type='png', dpi=fig.dpi, bbox_inches='tight')

