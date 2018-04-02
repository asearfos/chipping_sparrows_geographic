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
Load in information for all the Chipping Sparrow audio files on Macaulay Library as of 2018-03-28 
"""


"""
Macaulay Library Data
"""

data1 = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\SongDataSearchResults\ML_2018-03-28T18" \
        "-14_Spizella_passerina_Audio.csv"

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
    rec_time = ':'.join((line[10][0:-2], line[10][-2:len(line[10])])) if len(line[10]) > 0 else None
    recordist = line[5] if len(line[5]) > 0 else None

    if len(line[31]) > 0 and len(line[32]) > 0:
        comments = "; ".join([line[31], line[32]])
    else:
        if len(line[31]) > 0:
            comments = line[31]
        elif len(line[33]) > 0:
            comments = line[32]
        else:
            comments = None

    fields = (catalog_number, latitude, longitude, day, month, year, rec_time, recordist, comments)
    cursor.execute('INSERT INTO asearfos.AllChippingSparrowsAudio_FromML_AsOf20180328 (CatalogNo, Latitude, Longitude, '
                   'RecordingDay, RecordingMonth, RecordingYear, RecordingTime, Recordist, RecordingComments) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()
