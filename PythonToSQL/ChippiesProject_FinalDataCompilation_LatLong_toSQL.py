import pymysql as sql
import os
import csv
from datetime import datetime
import time
import re

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()

"""
add any information I have for Chippies to a sql table ChippingSparrows_FinalDataCompilation
"""


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
    filename = data1


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database, filename)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase, FromCSV) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
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
    filename = data2

    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database, filename)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase, FromCSV) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
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
    filename = data3

    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database, filename)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase, FromCSV) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
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
    filename = data4

    if len(line[19]) > 0:
        time_twelve = line[19]
        am_pm = line[20]
        datetime_time = datetime.strptime(" ".join([time_twelve, am_pm]), "%I:%M %p")
        rec_time = datetime.strftime(datetime_time, "%H:%M")
    else:
        rec_time = None

    if line[8] != "Not specified" and (line[23] != "Comments:N/A" or len(line[23]) > 0):
        comments = "; ".join([line[8], line[23]])
    else:
        if line[8] != "Not specified":
            comments = line[8]
        elif line[23] != "Comments:N/A" and len(line[23]) > 0:
            comments = line[23]
        else:
            comments = None


    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database, filename)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase, FromCSV) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()

"""
Xeno-Canto data from excel file
"""

data5 = "C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/chipping sparrow new " \
        "recording/fromXC/XC_chippingSparrow_song_AsOf07042017_newDataDownloaded/xeno" \
        "-canto_chippingSparrow_song_AsOf07042017_final.csv"

fin = csv.reader(open(data5, 'r'))
header = next(fin)

for line in fin:
    line = [item.strip() for item in line]

    catalog_number = "XC" + line[14] if len(line[14]) > 0 else None
    latitude = line[8] if len(line[8]) > 0 else None
    longitude = line[9] if len(line[9]) > 0 else None

    if len(line[4]) > 0:
        try:
            date = datetime.strptime(line[4], "%m/%d/%Y")
            day = date.day
            month = date.month
            year = date.year
        except ValueError:
            day = None
            month = line[4].split('-')[1].lstrip('0')
            year = line[4][:4]
    else:
        date, day, month, year = None, None, None, None

    if len(line[5]) > 0 and line[5] != '?':
        if ":" not in line[5]:
            rec_time = ':'.join((line[5][0:-2], line[5][-2:len(line[5])]))
        elif "am" or "pm" or "AM" or "PM" in line[5]:
            rec_time = line[5][:line[5].find(':')+3]
        else:
            rec_time = line[5]
    else:
        rec_time = None

    recordist = line[3] if len(line[3]) > 0 else None
    comments = line[12] if len(line[12]) > 0 else None
    database = 'Xeno-Canto'
    filename = data5

    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments, database, filename)
    cursor.execute('INSERT INTO asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments, '
                   'FromDatabase, FromCSV) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


# """
# Xeno-Canto data from server SongMetaData (and one that is manually entered since not on server database)
# """
#
# cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
#                "select concat('XC', XenoCantoCatalogNumber), RecordingLatitude, RecordingLongitude, 'Xeno-Canto' "
#                "from BirdSong.SongMetaData "
#                "where XenoCantoCatalogNumber in ("
#                "select right(CatalogNo, length(CatalogNo)-2) "
#                "from asearfos.SongDataFiles_AMS "
#                "where FromDatabase = 'Xeno-Canto');")
#
# cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, Latitude, Longitude, FromDatabase) "
#                "values ('XC47096', '42.9116459119664', '-88.4770653247506', 'Xeno-Canto');")
#
# conn.commit()

"""
old data pulled from my table in server
"""
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, RecordingDay, RecordingMonth, "
               "RecordingYear, RecordingTime, Latitude, Longitude, FromDatabase, FromCSV) "
               "select CatalogNo, day(Day), month(Day), Year(Day), maketime(left(TimeOfDay, length(TimeOfDay)-2), "
               "right(TimeOfDay, 2), '00'), Latitude, Longitude, 'old', ExcelFile "
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
                   "and FromDatabase = 'old' or FromDatabase = 'missing') "
               "and ExcelFile like '%location%';")

# next get information from listing from excel file like 'ttest' --> 25 entries
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, RecordingDay, RecordingMonth, "
               "RecordingYear, RecordingTime, Latitude, Longitude, FromDatabase, FromCSV) "
               "select CatalogNo, day(Day), month(Day), Year(Day), maketime(left(TimeOfDay, length(TimeOfDay)-2), "
               "right(TimeOfDay, 2), '00'), Latitude, Longitude, 'old', ExcelFile "
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
                   "and FromDatabase = 'old' or FromDatabase = 'missing') "
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
                       "and FromDatabase = 'old' or FromDatabase = 'missing') "
                   "and ExcelFile like '%location%') "
               "and ExcelFile like '%ttest%';")

# last get information from listing from excel file like '719' --> 11 entries
cursor.execute("insert into asearfos.ChippingSparrows_FinalDataCompilation (CatalogNo, RecordingDay, RecordingMonth, "
               "RecordingYear, RecordingTime, Latitude, Longitude, FromDatabase, FromCSV) "
               "select CatalogNo, day(Day), month(Day), Year(Day), maketime(left(TimeOfDay, length(TimeOfDay)-2), "
               "right(TimeOfDay, 2), '00'), Latitude, Longitude, 'old', ExcelFile "
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
                   "and FromDatabase = 'old' or FromDatabase = 'missing') "
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
                       "and FromDatabase = 'old' or FromDatabase = 'missing') "
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
                       "and FromDatabase = 'old' or FromDatabase = 'missing') "
                   "and ExcelFile like '%ttest%') "
               "and ExcelFile like '%719%';")

conn.commit()

"""
Update Recordist for old files
"""
cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation "
               "set Recordist = 'Borror Lab' "
               "where FromDatabase = 'old' "
               "and	CatalogNo like '%.%'")

cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation "
               "set Recordist = 'Wan-chun Liu' "
               "where FromDatabase = 'old' "
               "and CatalogNo not REGEXP '^[0-9]+$' "
               "and CatalogNo not like '%.%'")

conn.commit()

"""
Add some missing Recordist information using the information from Macualay library. Note, only add 1st recordist not 
others listed in additional columns
"""

cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation as missing "
               "join (select CatalogNo, Recordist from asearfos.AllChippingSparrowsAudio_FromML_AsOf20180328) as info "
               "on missing.CatalogNo = info.CatalogNo "
               "set missing.Recordist = info.Recordist "
               "where missing.Recordist is Null;")

conn.commit()

"""
Update Regions based on Latitude and Longitude
"""

cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation "
               "set Region = 'south' "
               "where Latitude < 25;")

cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation "
               "set Region = 'east' "
               "where Latitude >= 25 and Longitude >= -90;")

cursor.execute("update asearfos.ChippingSparrows_FinalDataCompilation "
               "set Region = 'west' "
               "where Latitude >= 25 and Longitude <= -105;")

conn.commit()
