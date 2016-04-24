from urllib2 import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient

mc = MongoClient()
db = mc.vesselDB
db.iattc.drop()
iattcTable = db.iattc

def floatOrNan(string):
    try:
        floatValue = float(string)
    except ValueError:
        floatValue = float('nan')
    return floatValue

link = 'https://www.iattc.org//vesselregister/VesselList.aspx?List=RegVessels&Lang=ENG'
webpage = urlopen(link)
soup = BeautifulSoup(webpage.read())
tables = soup.find_all('table', id=lambda x: x and x.startswith('Flag_'))

results = []
for table in tables:
    headers = table.find_all('th')
    containsStringWeWantArray = [header.get_text() == 'IATTC Vessel Number' for header in headers]
    containsStringWeWant = any(containsStringWeWantArray)

    if containsStringWeWant:
        idString = table.get('id')
        idStringList = idString.replace('-','_').split('_')
        rows = table.find_all('tr')
        for row in rows:
            tableData = row.find_all('td')
            dataList = [cell.get_text() for cell in tableData]
            if len(dataList) == 6:
                dbRow = {"iattcVesselNumber": floatOrNan(dataList[0]), "name": dataList[1],
                         "lengthM": floatOrNan(dataList[2]), "fishHoldVolumeM3": floatOrNan(dataList[3]),
                         "carryingCapacityT": floatOrNan(dataList[4]), "flag": idStringList[1],
                         "gear": idStringList[3], "link": link}
                iattcTable.insert_one(dbRow)

