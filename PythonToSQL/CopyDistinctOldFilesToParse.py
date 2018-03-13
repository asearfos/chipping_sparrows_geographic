import pymysql as sql
import shutil
import os

conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos', password='')
cursor = conn.cursor()

# find any files that are in our compiled list of "old" songs (OldChippingSparrowData_fromNicole) that are not in our
# already pulled files from eBird, ML, and XC (SongDataFile_AMS). Essentially any files from 'old' that I have both
# information and data for but don't already have.
cursor.execute(
                "select FileLocation, FileName from asearfos.SongDataFiles_AMS "
                    "where CatalogNo in ("
                        "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                        "from asearfos.OldChippingSparrowData_fromNicole "
                        "inner join asearfos.SongDataFiles_AMS on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo)"
                    "and CatalogNo not in (" 
                        "select CatalogNo "
                        "from asearfos.SongDataFiles_AMS "
                        "group by CatalogNo having count(*) > 1) "
                    "and FromDatabase = 'old'"
                "order by CatalogNo, FromDatabase desc;")

# put copies of all the old files into subdirectories to be easily passed through Chipper (10 per folder)
newLocation = 'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation\chipping sparrow old ' \
              'recordings bouts/old_bouts_'

i = 0
folder = 1
for row in cursor.fetchall():
    boutDirectory = (newLocation + str(folder) + '/')
    i = i + 1
    if not os.path.exists(boutDirectory):
        os.makedirs(boutDirectory)
    shutil.copy("/".join(row[:]), (newLocation + str(folder) + '/'))
    if i % 10 == 0:
        folder += 1


