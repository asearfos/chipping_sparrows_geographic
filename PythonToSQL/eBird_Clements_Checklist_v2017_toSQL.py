import pymysql as sql
import csv

fileWithPassword = open('C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\creanzaLabServer_searfoamPassword.txt', 'r')
conn = sql.connect('creanza-lab-server.cas.vanderbilt.edu', user='asearfos',
                   password=fileWithPassword.read().strip(), use_unicode=True, charset="utf8")
cursor = conn.cursor()

"""
Load in eBird/Clements Checklist v2017 from http://www.birds.cornell.edu/clementschecklist/download/ 
"""

# Macaulay Library data
ClementsChecklist = 'C:/Users/abiga\Documents\GRADUATEWORK\CREANZA_LAB\PythonToSQL\eBird-Clements-integrated' \
                    '-checklist-v2017.csv'

fin = csv.reader(open(ClementsChecklist, 'r'))
header = next(fin)

# prev_eBirdSpeciesCode = None
for line in fin:
    line = [item.strip() for item in line]

    eBirdSpeciesCode = line[0] if len(line[0]) > 0 else None
    # if eBirdSpeciesCode is None:
    #     eBirdSpeciesCode = prev_eBirdSpeciesCode

    sort_v2017 = line[1] if len(line[1]) > 0 else None
    category = line[2] if len(line[2]) > 0 else None
    EnglishName = line[3] if len(line[3]) > 0 else None

    scientificName = str.split(line[4], ' ') if len(str.split(line[4], ' ')) > 0 else None
    genus = scientificName[0]

    if category == 'hybrid':
        species = " ".join(scientificName)
        subspecies = None
    else:
        species = scientificName[1]
        subspecies = None if len(scientificName) == 2 else " ".join(scientificName[2:])

    range = line[5] if len(line[5]) > 0 else None
    order = line[6] if len(line[6]) > 0 else None
    familyLong = line[7] if len(line[7]) > 0 else None
    try:
        family, commonName = str.split(familyLong[:-1], '(')
    except:
        family, commonName = None, None
    eBirdSpeciesGroup = line[8] if len(line[8]) > 0 else None
    extinct = line[9] if len(line[9]) > 0 else None
    extinctYear = line[10] if len(line[10]) > 0 else None
    year = '2017'
    # prev_eBirdSpeciesCode = eBirdSpeciesCode

    fields = (eBirdSpeciesCode, sort_v2017, category, EnglishName, genus, species, subspecies, order, family,
              commonName, eBirdSpeciesGroup, extinct, extinctYear, range, year)
    cursor.execute('INSERT INTO asearfos.ClementsChecklist (eBirdSpeciesCode2017, Sort_v2017, Category, EnglishName, '
                   'TaxonGenus, TaxonSpecies, TaxonSubspecies, TaxonOrder, TaxonFamily, CommonName, eBirdSpecies, Extinct, ExtinctYear, '
                   'Location, ClementsChecklistVersion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', fields)
conn.commit()


