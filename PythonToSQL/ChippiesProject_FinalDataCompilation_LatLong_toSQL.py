import pymysql as sql
import os
import csv
from datetime import datetime
import time

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()


"""
Macaulay Library Data
"""

data1 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new " \
        "recording/fromML\ML_Order_30095672017_Jul_06_17_11_08\ML_Order_30095672017_Jul_06_17_11_08.csv"

fin = csv.reader(open(data1, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    catalog_number = line[0] if len(line[0]) > 0 else None
    latitude = line[15] if len(line[15]) > 0 else None
    longitude = line[16] if len(line[16]) > 0 else None
    day = line[9] if len(line[9]) > 0 else None
    month = line[8] if len(line[8]) > 0 else None
    year = line[7] if len(line[7]) > 0 else None
    # date =
    rec_time = ':'.join((line[10][0:-2], line[10][-2:len(line[10])])) if len(line[10]) > 0 else None
    recordist = line[6] if len(line[6]) > 0 else None
    comments = line[38] if len(line[38]) > 0 else None
    database = 'Macaulay Library'


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


data2 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new recording/fromML\more macaulay " \
        "library from Nicole\moreMacaulayLibraryFromNicole_information.csv"

fin = csv.reader(open(data2, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    catalog_number = line[0] if len(line[0]) > 0 else None
    latitude = line[15] if len(line[15]) > 0 else None
    longitude = line[16] if len(line[16]) > 0 else None
    day = line[9] if len(line[9]) > 0 else None
    month = line[8] if len(line[8]) > 0 else None
    year = line[7] if len(line[7]) > 0 else None
    # date =
    rec_time = ':'.join((line[10][0:-2], line[10][-2:len(line[10])])) if len(line[10]) > 0 else None
    recordist = line[5] if len(line[5]) > 0 else None
    comments = line[31] if len(line[31]) > 0 else None
    database = 'Macaulay Library'


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


"""
eBird
"""

data3 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new " \
        "recording/fromEBird\eBird_extractedWithSoundflower\eBird_MLCatNum_2017-12-19_Spizella_passerina_Audio.csv"

fin = csv.reader(open(data3, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    catalog_number = line[0] if len(line[0]) > 0 else None
    latitude = line[15] if len(line[15]) > 0 else None
    longitude = line[16] if len(line[16]) > 0 else None
    day = line[9] if len(line[9]) > 0 else None
    month = line[8] if len(line[8]) > 0 else None
    year = line[7] if len(line[7]) > 0 else None
    # date =
    rec_time = ':'.join((line[10][0:-2], line[10][-2:len(line[10])])) if len(line[10]) > 0 else None
    recordist = line[5] if len(line[5]) > 0 else None
    comments = line[31] if len(line[31]) > 0 else None
    database = 'eBird'


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


data4 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new " \
        "recording/fromEBird\eBird_MLCatNum_ChippingSparrows_asOf07142017_fromMatthewYoung" \
        "\eBird_MLCatNum_fromMatthewYoung_locationData_final.csv"

fin = csv.reader(open(data4, 'r', encoding="utf8"))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    catalog_number = line[0] if len(line[0]) > 0 else None
    latitude = line[9] if len(line[9]) > 0 else None
    longitude = line[10] if len(line[10]) > 0 else None
    day = line[17] if len(line[17]) > 0 else None
    month = time.strptime(line[16], '%b').tm_mon if len(line[16]) > 0 else None
    year = line[18] if len(line[18]) > 0 else None
    # date =
    recordist = line[3] if len(line[3]) > 0 else None
    database = 'eBird'

    if len(line[19]) > 0:
        time_twelve = line[19]
        am_pm = line[20]
        datetime_time = datetime.strptime(" ".join([time_twelve, am_pm]), "%I:%M %p")
        rec_time = datetime.strftime(datetime_time, "%H:%M")
    else:
        rec_time = None

    if len(line[8]) > 0 and len(line[23]) > 0:
        comments = " ".join([line[8], line[23]])
    else:
        if len(line[8]) > 0:
            comments = line[8]
        elif len(line[23]) > 0:
            comments = line[23]
        else:
            comments = None


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


"""
Xeno-Canto data from server SongMetaData (and one that is manually entered since not on server database)
"""

cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
               "select concat('XC', XenoCantoCatalogNumber), RecordingLatitude, RecordingLongitude, 'Xeno-Canto' "
               "from BirdSong.SongMetaData "
               "where XenoCantoCatalogNumber in ("
               "select right(CatalogNo, length(CatalogNo)-2) "
               "from asearfos.SongDataFiles_AMS "
               "where FromDatabase = 'Xeno-Canto');")

cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
               "values ('XC47096', '42.9116459119664', '-88.4770653247506', 'Xeno-Canto');")

conn.commit()


"""
old data pulled from my table in server
"""

# first get information from listing from excel file like 'location' --> 607 entries
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
               "select CatalogNo, Latitude, Longitude, 'old' "
               "from asearfos.OldChippingSparrowData_fromNicole "
               "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                   "select SongDataFiles_AMS.CatalogNo "
                   "from asearfos.SongDataFiles_AMS "
                   "where CatalogNo in ("
                       "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                       "from asearfos.OldChippingSparrowData_fromNicole "
                       "inner join asearfos.SongDataFiles_AMS "
                       "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                   "and CatalogNo not in ("
                       "select CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "group by CatalogNo having count(*) > 1) "
                   "and FromDatabase = 'old') "
               "and ExcelFile like '%location%';")

# next get information from listing from excel file like 'ttest' --> 25 entries
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
               "select CatalogNo, Latitude, Longitude, 'old' "
               "from asearfos.OldChippingSparrowData_fromNicole "
               "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                   "select SongDataFiles_AMS.CatalogNo "
                   "from asearfos.SongDataFiles_AMS "
                   "where CatalogNo in ("
                       "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                       "from asearfos.OldChippingSparrowData_fromNicole "
                       "inner join asearfos.SongDataFiles_AMS "
                       "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                   "and CatalogNo not in ("
                       "select CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "group by CatalogNo having count(*) > 1) "
                   "and FromDatabase = 'old') "
               "and OldChippingSparrowData_fromNicole.CatalogNo not in ("  # not in previous query
                   "select CatalogNo "
                   "from asearfos.OldChippingSparrowData_fromNicole "
                   "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                       "select SongDataFiles_AMS.CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "where CatalogNo in ("
                           "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                           "from asearfos.OldChippingSparrowData_fromNicole "
                           "inner join asearfos.SongDataFiles_AMS "
                           "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                       "and CatalogNo not in ("
                           "select CatalogNo "
                           "from asearfos.SongDataFiles_AMS "
                           "group by CatalogNo having count(*) > 1) "
                       "and FromDatabase = 'old') "
                   "and ExcelFile like '%location%') "
               "and ExcelFile like '%ttest%';")

# last get information from listing from excel file like '719' --> 11 entries
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
               "select CatalogNo, Latitude, Longitude, 'old' "
               "from asearfos.OldChippingSparrowData_fromNicole "
               "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                   "select SongDataFiles_AMS.CatalogNo "
                   "from asearfos.SongDataFiles_AMS "
                   "where CatalogNo in ("
                       "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                       "from asearfos.OldChippingSparrowData_fromNicole "
                       "inner join asearfos.SongDataFiles_AMS "
                       "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                   "and CatalogNo not in ("
                       "select CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "group by CatalogNo having count(*) > 1) "
                   "and FromDatabase = 'old') "
               "and OldChippingSparrowData_fromNicole.CatalogNo not in ("  # not in previous query 
                   "select CatalogNo "
                   "from asearfos.OldChippingSparrowData_fromNicole "
                   "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                       "select SongDataFiles_AMS.CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "where CatalogNo in ("
                           "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                           "from asearfos.OldChippingSparrowData_fromNicole "
                           "inner join asearfos.SongDataFiles_AMS "
                           "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                       "and CatalogNo not in ("
                           "select CatalogNo "
                           "from asearfos.SongDataFiles_AMS "
                           "group by CatalogNo having count(*) > 1) "
                       "and FromDatabase = 'old') "
                   "and ExcelFile like '%location%') "
               "and OldChippingSparrowData_fromNicole.CatalogNo not in ("  
                   "select CatalogNo "
                   "from asearfos.OldChippingSparrowData_fromNicole "
                   "where OldChippingSparrowData_fromNicole.CatalogNo in ("
                       "select SongDataFiles_AMS.CatalogNo "
                       "from asearfos.SongDataFiles_AMS "
                       "where CatalogNo in ("
                           "select distinct asearfos.OldChippingSparrowData_fromNicole.CatalogNo "
                           "from asearfos.OldChippingSparrowData_fromNicole "
                           "inner join asearfos.SongDataFiles_AMS "
                           "on asearfos.OldChippingSparrowData_fromNicole.CatalogNo = asearfos.SongDataFiles_AMS.CatalogNo) "
                       "and CatalogNo not in ("
                           "select CatalogNo "
                           "from asearfos.SongDataFiles_AMS "
                           "group by CatalogNo having count(*) > 1) "
                       "and FromDatabase = 'old') "
                   "and ExcelFile like '%ttest%') "
               "and ExcelFile like '%719%';")

conn.commit()