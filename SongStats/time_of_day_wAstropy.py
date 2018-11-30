import pytz
from astropy.io import ascii
import astropy.units as u
from astropy.coordinates import EarthLocation, Angle
from astroplan import Observer
from tzwhere import tzwhere
from astropy.table import Table


tz = tzwhere.tzwhere()
from astropy.time import Time

"""
Create csv file with each song file categorized as before or after sunrise, twilights, and noon. 
Note, only ended up using, before sunrise, after sunrise and afternoon.
"""
#read in data
table = ascii.read("C:/Users/abiga\Box "
                   "Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation"
                   "\FinalDataframe_CombinedTables_withReChipper_thenWithReExportedAs44100Hz_LogTransformed.csv",
                   delimiter=',')

relative_sunrise = []
relative_civil = []
relative_nautical = []
relative_astronomical = []

for i in range(len(table)):
    lat = Angle(table['Latitude'][i], u.deg)
    lon = Angle(table['Longitude'][i], u.deg)

    location = EarthLocation.from_geodetic(lon, lat)

    timezone = tz.tzNameAt(lat.deg, lon.deg)

    if timezone is not None:
        obs = Observer(location=location, timezone=pytz.timezone(timezone))

        if (table['RecordingYear'].data[i] != '--'
            and table['RecordingDay'].data[i] != '--'
            and table['RecordingTime'].data[i] != '--'):

            rec_datetime = list(map(str, [int(table['RecordingYear'].data[i]),
                                      int(table['RecordingMonth'].data[i]),
                                      int(table['RecordingDay'].data[i]),
                                      table['RecordingTime'].data[i]]))
            try:
                local_time = Time("{0}-{1}-{2} {3}".format(*rec_datetime)).datetime
                localized_time = pytz.timezone(timezone).localize(local_time)
                astropy_time = Time(localized_time)

                noon_time = Time("{0}-{1}-{2} 12:00:00".format(*rec_datetime)).datetime
                localized_noon = pytz.timezone(timezone).localize(noon_time)
                noon = Time(localized_noon)

                sunrise = obs.sun_rise_time(astropy_time, which='nearest')
                astro = obs.twilight_morning_astronomical(astropy_time, which='nearest')
                civil = obs.twilight_morning_civil(astropy_time, which='nearest')
                nautical = obs.twilight_morning_nautical(astropy_time, which='nearest')

                if noon < astropy_time:
                    relative_sunrise.append('after noon')
                    relative_astronomical.append('after noon')
                    relative_civil.append('after noon')
                    relative_nautical.append('after noon')
                else:
                    if sunrise < astropy_time:
                        relative_sunrise.append('after sunrise')
                    else:
                        relative_sunrise.append('before sunrise')
                    if civil < astropy_time:
                        relative_civil.append('after civil')
                    else:
                        relative_civil.append('before civil')
                    if nautical < astropy_time:
                        relative_nautical.append('after nautical')
                    else:
                        relative_nautical.append('before nautical')
                    if astro < astropy_time:
                        relative_astronomical.append('after astronomical')
                    else:
                        relative_astronomical.append('before astronomical')

            except ValueError:
                relative_sunrise.append('--')
                relative_astronomical.append('--')
                relative_civil.append('--')
                relative_nautical.append('--')
        else:
            relative_sunrise.append('--')
            relative_astronomical.append('--')
            relative_civil.append('--')
            relative_nautical.append('--')
    else:
        relative_sunrise.append('--')
        relative_astronomical.append('--')
        relative_civil.append('--')
        relative_nautical.append('--')


table = Table([table['CatalogNo'], relative_sunrise, relative_civil, relative_nautical, relative_astronomical],
              names=('CatalogNo', 'Sunrise', 'CivilTwilight', 'NauticalTwilight', 'AstronomicalTwilight'))
with open('C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/StatsOfFinalData_withReChipperReExported'
          '/TimeAnalysis/FinalData_LogTransformed_relativeToSunriseTwilightsNoon.csv', 'wb') as outfile:
    ascii.write(table, format='csv', output=outfile)
