from pymongo import MongoClient

mc = MongoClient()
db = mc.vesselDB
db.combined.drop()
combinedTable = db.combined

ftPerM = 3.28084

iattcData = db.iattc.find()
for row in iattcData:
    formattedRow = {'name': row['name'], 'lengthFt': round(row['lengthM'] * ftPerM), 'flag': row['flag'],
                    'link': row['link'], 'db': 'iattc', 'dbId': row['_id']}
    combinedTable.insert_one(formattedRow)

iuuData = db.iuu.find()
for row in iuuData:
    lengthValueUnit = row['Length']
    unit = lengthValueUnit.lstrip(',.0123456789')
    afterNumber = unit.split()
    value = lengthValueUnit[0:len(lengthValueUnit) - len(unit)].replace(',', '.')
    if afterNumber:
        unit = afterNumber[-1].lower()
    else:
        unit = ''
    if value:
        value = float(value)
    if unit == 'metres':
        value = value * ftPerM
    elif unit == 'feet':
        value = value
    else:
        if value:
            raise ValueError('Unknown unit')
    if value:
        lengthFt = round(value)
    else:
        lengthFt = float('nan')
    formattedRow = {'name': row['RFMO Vessel Name'], 'lengthFt': lengthFt, 'flag': row['Current Flag'],
                    'link': row['link'], 'db': 'iuu', 'dbId': row['_id']}
    combinedTable.insert_one(formattedRow)