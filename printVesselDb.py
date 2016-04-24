from pymongo import MongoClient

mc = MongoClient()
db = mc.vesselDB
collectionNames = db.collection_names()

for name in collectionNames:
    print name
    collection = db[name].find()
    for row in collection:
        print row
    print