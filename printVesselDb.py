from pymongo import MongoClient

mc = MongoClient()
db = mc.vesselDB
collectionNames = db.collection_names()

print collectionNames