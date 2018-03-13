import pymysql as sql
import csv

conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos', password='')
cursor = conn.cursor()


"""
Old Recordings
"""
# data1 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\OldRecordingInfo\chipping sparrow old recordings date " \
#        "time location.csv"
data1 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow old " \
        "recordings\OldRecordingInfo\OldChippingSparrowData_fromNicole_SQLDatabase\chipping sparrow old recordings " \
        "date time location.csv"

fin = csv.reader(open(data1, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    filename = line[0] if len(line[0]) > 0 else None
    index = line[1] if len(line[1]) > 0 else None
    catalog_number = line[2] if len(line[2]) > 0 else None
    catalog_no = line[3] if len(line[3]) > 0 else None
    day = line[4] if len(line[4]) > 0 and '?' not in line[4] else None
    year = line[5] if len(line[5]) > 0 else None
    time = line[6] if len(line[6]) > 0 else None
    latitude = line[7] if len(line[7]) > 0 else None
    longitude = line[8] if len(line[8]) > 0 else None
    excel_file = data1


    fields = (filename, index, catalog_number, catalog_no, day, year, time, latitude, longitude, excel_file)
    cursor.execute('INSERT INTO asearfos.OldChippingSparrowData_fromNicole (FileName, ID, CatalogNumber, CatalogNo, '
                   'Day, Year, TimeOfDay, Latitude, Longitude, ExcelFile) VALUES (%s, %s, %s, %s, STR_TO_DATE(%s, '
                   '"%%m/%%d/%%Y"), %s, %s, %s, %s, %s);', fields)
conn.commit()

"""
719 recordings
"""
# data2 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\OldRecordingInfo\old chipping sparrow analysis 719 " \
#        "birds with labels.csv"
data2 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow old " \
        "recordings\OldRecordingInfo\OldChippingSparrowData_fromNicole_SQLDatabase\old chipping sparrow analysis 719 " \
        "birds with labels.csv"

fin = csv.reader(open(data2, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    filename = line[0] if len(line[0]) > 0 else None
    catalog_number = line[1] if len(line[1]) > 0 else None
    catalog_no = line[2] if len(line[2]) > 0 else None
    year = line[3] if len(line[3]) > 0 else None
    latitude = line[4] if len(line[4]) > 0 else None
    longitude = line[5] if len(line[5]) > 0 else None
    excel_file = data2


    fields = (filename, catalog_number, catalog_no, year, latitude, longitude, excel_file)
    cursor.execute('INSERT INTO asearfos.OldChippingSparrowData_fromNicole (FileName, CatalogNumber, CatalogNo, Year, Latitude, Longitude, ExcelFile) VALUES (%s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()



"""
Excerpts for ttest
"""
# data3 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\OldRecordingInfo\chipping sparrow excerpts for " \
#         "ttest.csv"
data3 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow old " \
        "recordings\OldRecordingInfo\OldChippingSparrowData_fromNicole_SQLDatabase\chipping sparrow excerpts for " \
        "ttest.csv"

fin = csv.reader(open(data3, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    index = line[1] if len(line[1]) > 0 else None
    filename = line[2] if len(line[2]) > 0 else None
    catalog_no = line[3] if len(line[3]) > 0 else None
    day = line[4] if len(line[4]) > 0 and '?' not in line[4] else None
    year = line[5] if len(line[5]) > 0 else None
    time = line[6] if len(line[6]) > 0 else None
    latitude = line[7] if len(line[7]) > 0 else None
    longitude = line[8] if len(line[8]) > 0 else None
    excel_file = data3


    fields = (filename, index, catalog_no, day, year, time, latitude, longitude, excel_file)
    cursor.execute('INSERT INTO asearfos.OldChippingSparrowData_fromNicole (FileName, ID, CatalogNo, Day, Year, '
                   'TimeOfDay, Latitude, Longitude, ExcelFile) '
                   'VALUES (%s, %s, %s, STR_TO_DATE(%s,"%%m/%%d/%%Y"), %s, %s, %s, %s, %s);', fields)
conn.commit()


"""
Update table to fill nulls for CatalogNumber and CatalogNo
"""

cursor.execute('update asearfos.OldChippingSparrowData_fromNicole set CatalogNumber = CatalogNo WHERE '
               'OldChippingSparrowDataID NOT IN '
               '(SELECT data.OldChippingSparrowDataID FROM (SELECT * FROM asearfos.OldChippingSparrowData_fromNicole) as data WHERE (CatalogNumber is not Null and CatalogNo is not Null) '
               'and CatalogNumber != CatalogNo) AND CatalogNo IS NULL AND CatalogNumber IS NOT NULL;')

cursor.execute('update asearfos.OldChippingSparrowData_fromNicole set CatalogNumber = CatalogNo WHERE '
               'OldChippingSparrowDataID NOT IN '
               '(SELECT data.OldChippingSparrowDataID FROM (SELECT * FROM asearfos.OldChippingSparrowData_fromNicole) as data WHERE (CatalogNumber is not Null and CatalogNo is not Null) '
               'and CatalogNumber != CatalogNo) AND CatalogNo IS NOT NULL AND CatalogNumber IS NULL;')

"""
Update latitude, longitude, and date of the old table with the server information for Xeno-Canto data
"""

cursor.execute("UPDATE asearfos.OldChippingSparrowData_fromNicole inner join BirdSong.SongMetaData "
               "ON cast(right(CatalogNo, length(CatalogNo)-2) as signed) = XenoCantoCatalogNumber "
               "and CatalogNo Like 'xc%' "
               "SET Latitude = RecordingLatitude, Longitude = RecordingLongitude, Day = date(RecordingDateTime);")

"""
Remove extra quotes from filenames
"""

cursor.execute('update asearfos.OldChippingSparrowData_fromNicole as old '
               'set old.FileName = trim(both "\'" from old.FileName);')

"""
Updating CatalogNo's in rows that CatalogNo != the first substring of the FileName before a space
"""
#subset where old.ID equals the substring; a couple of these files must be excluded
cursor.execute("update asearfos.OldChippingSparrowData_fromNicole as old "
               "set old.CatalogNo = old.ID "
               "where old.CatalogNo != substring_index(old.FileName, ' ', 1) "
               "and old.ID = substring_index(old.FileName, ' ', 1) "
               "and old.FileName not in('xc16983-07-05-2007-michigan-US bout.wav', 'bird2. fivesyll.wav', 'bird1. fivesyll.wav');")

#subset where ID is NULL, the FileName has at least two . in the name, and not bird1 or bird2 files
cursor.execute("update asearfos.OldChippingSparrowData_fromNicole as old "
               "set old.CatalogNo = substring_index(old.FileName, ' ', 1) "
               "where old.CatalogNo != substring_index(old.FileName, ' ', 1) "
               "and old.ID is NULL "
               "and old.FileName like '%.%.%' "
               "and old.FileName not in('bird2. fivesyll.wav', 'bird1. fivesyll.wav');")

#update one CatalogNo that is wrong - still has fivesyll in it
cursor.execute("update asearfos.OldChippingSparrowData_fromNicole as old "
               "set old.CatalogNo = substring_index(old.FileName, ' ', 1) "
               "where old.CatalogNo like ('1_395664508_4_28_10_49_14 fivesyllwav');")

#update one catalogNo that is still NULL
cursor.execute("update asearfos.OldChippingSparrowData_fromNicole as old "
               "set old.CatalogNo = substring_index(old.FileName, ' ', 1) "
               "where old.CatalogNo is NULL;")

conn.commit()