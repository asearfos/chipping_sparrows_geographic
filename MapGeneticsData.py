import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from mpl_toolkits.basemap import Basemap

#load in mitochondrial control region data to get locations and number of samples at each location
Haplo_Locations = pd.read_table("C:/Users/abiga\Box "
                                        "Sync\Abigail_Nicole\ChippiesProject\GeneticData\Mila_ControlRegionSeq"
                                        "\Mila_HaplotypeToLocation_correctedCA_allSamples.txt", delimiter="\t")

Haplo_Locations_wFreq = Haplo_Locations.groupby(['Latitude', 'Longitude']).size().reset_index(name='NumAtLocation')
print('mtDNA \n', Haplo_Locations_wFreq)
Haplo_Locations_wFreq.to_csv("C:/Users/abiga\Box Sync\Abigail_Nicole"
                            "\ChippiesProject\GeneticData"
                            "\Mila_ControlRegionSeq"
                            "\Mila_HaplotypeToLocation_correctedCA_allSamples_byCount.txt",
                             index=False)

#load in mitochondrial control region data to get locations and number of samples at each location
COI_Locations = pd.read_table("C:/Users/abiga\Box "
                                        "Sync\Abigail_Nicole\ChippiesProject\GeneticData\ChippingSparrow_Barcodes_2017"
                                        "\ChippingSparrow_BarcodesToLocations.txt", delimiter="\t")

COI_Locations_wFreq = COI_Locations.groupby(['Latitude', 'Longitude']).size().reset_index(name='NumAtLocation')
print('COI \n', COI_Locations_wFreq)
COI_Locations_wFreq.to_csv("C:/Users/abiga\Box Sync\Abigail_Nicole"
                            "\ChippiesProject\GeneticData"
                            "\ChippingSparrow_Barcodes_2017"
                            "\ChippingSparrow_BarcodesToLocations_byCount.txt",
                             index=False)

quit()

# Set the dimension of the figure
my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi, frameon=False)

#make the geographic background map
# m = Basemap(llcrnrlat=10, llcrnrlon=-140, urcrnrlat=65, urcrnrlon=-62)
m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
m.drawcoastlines(color='k', linewidth=1.5)
m.drawcountries(color='k', linewidth=1.5)
m.drawstates(color='gray')
m.drawmapboundary(fill_color='w', color='none')

#if you want the water and the land different colors
# m.fillcontinents(color="#cdc7bd", lake_color='#C5DBED')
# m.drawmapboundary(fill_color="#C5DBED")

#plot points at sampling locations with area proportional to number of samples at the location --> mtDNA
m.scatter(Haplo_Locations_wFreq['Longitude'], Haplo_Locations_wFreq['Latitude'], latlon=True,
          s=100*Haplo_Locations_wFreq['NumAtLocation'], label=None, zorder=10, c='#dfc27d', edgecolor='black',
          linewidth=1)

#plot points at sampling locations with area proportional to number of samples at the location --> COI
m.scatter(COI_Locations_wFreq['Longitude'], COI_Locations_wFreq['Latitude'], latlon=True,
          s=100*COI_Locations_wFreq['NumAtLocation'], label=None, zorder=10, c='#8c510a', edgecolor='black',
          linewidth=1)

#create a legend
for a in [1, 5, 20, 40]:
    plt.scatter([], [], c='k', s=100*a, label=str(a), edgecolors='k', linewidths=1)
plt.legend(scatterpoints=1, frameon=False, labelspacing=0.5, columnspacing=1,
           loc='lower right', fontsize=50)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/HaplotypePlots/" +
               'GeneticData_Locations_wFreq_allSamples_forPaper2' + '.pdf')

pdf.savefig(dpi=fig.dpi, orientation='landscape')
pdf.close()

plt.show()
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/HaplotypePlots/" +
#             'Haplo_Locations_wFreq_allSamples' + '.png',
#             type='png', dpi=fig.dpi, bbox_inches='tight')

