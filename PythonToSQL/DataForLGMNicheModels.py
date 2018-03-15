
import pymysql as sql
import shutil
import os
import csv

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip())

cursor = conn.cursor()

# EAST
cursor.execute("select CatalogNo, Latitude, Longitude "
               "from asearfos.FinalDataCompilation_LatLong "
               "where Region = 'east';")

rows = cursor.fetchall()
print(rows)

column_names = [i[0] for i in cursor.description]
newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_east_wHeader.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerow(column_names)
myFile.writerows(rows)
newFile.close()

cursor.execute("select Latitude, Longitude "
               "from asearfos.ChippingSparrows_FinalDataCompilation "
               "where Region = 'east';")

rows = cursor.fetchall()

newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_east.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerows(rows)
newFile.close()

# WEST
cursor.execute("select CatalogNo, Latitude, Longitude "
               "from asearfos.ChippingSparrows_FinalDataCompilation "
               "where Region = 'west';")

rows = cursor.fetchall()

column_names = [i[0] for i in cursor.description]
newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_west_wHeader.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerow(column_names)
myFile.writerows(rows)
newFile.close()

cursor.execute("select Latitude, Longitude "
               "from asearfos.ChippingSparrows_FinalDataCompilation "
               "where Region = 'west';")

rows = cursor.fetchall()

newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_west.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerows(rows)
newFile.close()

# SOUTH
cursor.execute("select CatalogNo, Latitude, Longitude "
               "from asearfos.ChippingSparrows_FinalDataCompilation "
               "where Region = 'south';")

rows = cursor.fetchall()

column_names = [i[0] for i in cursor.description]
newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_south_wHeader.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerow(column_names)
myFile.writerows(rows)
newFile.close()

cursor.execute("select Latitude, Longitude "
               "from asearfos.ChippingSparrows_FinalDataCompilation "
               "where Region = 'south';")

rows = cursor.fetchall()

newFile = open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\LastGlacialMaximumNicheModels"
               "/FinalDataCompilation_south.csv", 'w')
myFile = csv.writer(newFile, lineterminator='\n')
myFile.writerows(rows)
newFile.close()
