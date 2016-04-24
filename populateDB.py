from pymongo import MongoClient
mc = MongoClient()
db = mc.vesselDB

dbRow = {"vesselName": "Mr. Morgan","vesselServiceType": "Commercial fishing vessel","length":60}

db.vessels.insert_one(dbRow)

dbRow = {"vesselName": "Mr. Morgan","vesselServiceType": "Commercial fishing vessel","length":68}

db.vessels.insert_one(dbRow)

dbRow = {"vesselName": "Golden Chalice","vesselServiceType": "Commercial fishing vessel","length":55}

db.vessels.insert_one(dbRow)

dbRow = {"vesselName": "Miss Kelley II","vesselServiceType": "Trawl","length":50}

db.vessels.insert_one(dbRow)

data=db.vessels.find()
for record in data:
    print record
