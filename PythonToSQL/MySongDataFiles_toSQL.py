import pymysql as sql
import os

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip())
cursor = conn.cursor()

"""
Load in all song files I have from Xeno-Canto, eBird, Macaulay Library, and from Nicole's old hard-drive ('missing') 
to a sql table SongDataFiles_AMS
"""

# Macaulay Library data
Database_ML = 'Macaulay Library'
FileLocations_ML = ['C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new '
                    'recording/fromML\ML_Order_30095672017_Jul_06_17_11_08',
                    'C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new '
                    'recording/fromML\more macaulay library from Nicole']

for j in FileLocations_ML:
    (_, _, files_ML) = next(os.walk(j), (None, None, []))
    filenames_ML = [f for f in files_ML if f.endswith('.wav') or f.endswith('.mp3') or f.endswith('.WAV')]
    for i in filenames_ML:
        FileName = i
        Database = Database_ML
        FileLocation = j


        fields = (FileName, Database, FileLocation)
        cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
                       'VALUES (%s, %s, %s);', fields)
    conn.commit()


# Xeno-canto data
Database_XC = 'Xeno-Canto'
FileLocations_XC = ["C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new " \
                    "recording/fromXC\XC_chippingSparrow_song_AsOf07042017_newDataDownloaded",
                    "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new "
                    "recording/fromXC\XC_chippingSparrow_inBackground"]

for m in FileLocations_XC:
    (_, _, files_XC) = next(os.walk(m), (None, None, []))
    filenames_XC = [f for f in files_XC if f.endswith('.wav') or f.endswith('.mp3')]
    for i in filenames_XC:
        FileName = i
        Database = Database_XC
        FileLocation = m

        fields = (FileName, Database, FileLocation)
        cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
                       'VALUES (%s, %s, %s);', fields)
    conn.commit()


# eBird data
# Database_eBird = 'eBird'
# FileLocation_eBird = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new " \
#                      "recording/fromEBird\eBird_MLCatNum_ChippingSparrows_asOf07142017_fromMatthewYoung"
# (_, _, files_eBird) = next(os.walk(FileLocation_eBird), (None, None, []))
# filenames_eBird = [f for f in files_eBird if not f.endswith('.txt')]
#
# for i in filenames_eBird:
#     FileName = i
#     Database = Database_eBird
#     FileLocation = FileLocation_eBird
#
#     fields = (FileName, Database, FileLocation)
#     cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
#                    'VALUES (%s, %s, %s);', fields)
# conn.commit()

# eBird data
Database_eBird = 'eBird'
FileLocations_eBird = ["C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new "
                       "recording/fromEBird\eBird_MLCatNum_ChippingSparrows_asOf07142017_fromMatthewYoung",
                       "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new "
                       "recording/fromEBird\eBird_extractedWithSoundflower",
                       "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow new "
                       "recording/fromEBird\eBird_extractedWithSoundflower_round2"]

for k in FileLocations_eBird:
    (_, _, files_eBird) = next(os.walk(k), (None, None, []))
    filenames_eBird = [f for f in files_eBird if not (f.endswith('.txt') or f.endswith('.csv'))]
    for i in filenames_eBird:
        FileName = i
        Database = Database_eBird
        FileLocation = k

        fields = (FileName, Database, FileLocation)
        cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
                       'VALUES (%s, %s, %s);', fields)
    conn.commit()



#  old recordings data
Database_old = 'old'
FileLocation_old = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow old recordings"
(_, _, files_old) = next(os.walk(FileLocation_old), (None, None, []))
filenames_old = [f for f in files_old if not f.endswith('.txt')]

for i in filenames_old:
    FileName = i
    Database = Database_old
    FileLocation = FileLocation_old

    fields = (FileName, Database, FileLocation)
    cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
                   'VALUES (%s, %s, %s);', fields)
conn.commit()

#  old data that was missing from any spreadsheets - got from Nicole's old hard drive
Database_missing = 'missing'
FileLocation_missing = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\chipping sparrow missing recordings"
(_, _, files_missing) = next(os.walk(FileLocation_missing), (None, None, []))
filenames_missing = [f for f in files_missing if f.endswith('.wav')]

for i in filenames_missing:
    FileName = i
    Database = Database_missing
    FileLocation = FileLocation_missing

    fields = (FileName, Database, FileLocation)
    cursor.execute('INSERT INTO asearfos.SongDataFiles_AMS (FileName, FromDatabase, FileLocation) '
                   'VALUES (%s, %s, %s);', fields)
conn.commit()




# update catalog numbers
cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, '_', 1) "
               "where FromDatabase = 'Macaulay Library' "
               "and FileName like '%44k%';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, '.', 1) "
               "where FromDatabase = 'Macaulay Library' "
               "and FileName not like '%44k%' "
               "and FileName like '%.wav';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, '.', 1) "
               "where FromDatabase = 'eBird';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, ' ', 1) "
               "where FromDatabase = 'Xeno-Canto';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = substring_index(FileName, '-', 1) "
               "where FromDatabase = 'old' "
               "and FileName like '%xc%-%';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = substring_index(FileName, ' ', 1) "
               "where FromDatabase = 'old' "
               "and FileName like '%xc%' "
               "and FileName not in('xc16983-07-05-2007-michigan-US bout.wav');")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, ' ', 1) "
               "where FromDatabase = 'old' "
               "and FileName not like '%xc%' "
               "and FileName not like '% % %';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = substring_index(FileName, ' ', 1) "
               "where FromDatabase = 'old' "
               "and FileName not like '%xc%' "
               "and FileName like '%s1%';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set CatalogNo = substring_index(FileName, '.wav', 1) "
               "where FromDatabase = 'missing' "
               "and FileName like '%.wav';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = '106500' "
               "where FileName = '106500 s2 bout.wav';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = substring_index(FileName, ' bout.wav', 1) "
               "where FileName in('9713bQuabbinCorner nei bout.wav', 'fourth male bout.wav', 'third male bout.wav', "
               "'two days later2 bout.wav');")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = '132220' "
               "where FileName = 'b1s chipping sparrow 132220.wav';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = '9209' "
               "where FileName like '%9209.1%';")

cursor.execute("update asearfos.SongDataFiles_AMS "
               "set	CatalogNo = 'Boston12' "
               "where FileName like '%Boston12b%';")

conn.commit()
