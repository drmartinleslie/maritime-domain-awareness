from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
mc = MongoClient()
db = mc.vesselDB
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit')
def submit():
    vesselNameFromUser = request.args.get("vesselName")
    gearTypeFromUser = request.args.get("gearType")
    minLengthFromUser = request.args.get("minLength")
    maxLengthFromUser = request.args.get("maxLength")
    flagFromUser = request.args.get("flag")
    sortKeyFromUser = request.args.get("sortKey")

    query = {}

    if vesselNameFromUser:
        query["vesselName"] = vesselNameFromUser

    if minLengthFromUser and maxLengthFromUser:
        query["length"] = {"$gte": int(minLengthFromUser), "$lte": int(maxLengthFromUser)}

    if minLengthFromUser and (not maxLengthFromUser):
        query["length"] = {"$gte": int(minLengthFromUser)}

    if maxLengthFromUser and (not minLengthFromUser):
        query["length"] = {"$lte": int(maxLengthFromUser)}

    if gearTypeFromUser:
        query["gearType"] = gearTypeFromUser

    if flagFromUser:
        query["flag"] = flagFromUser

    results = db.combined.find(query).sort(sortKeyFromUser, 1) # 1 is ascending, -1 is descending

    if sortKeyFromUser == 'vesselName':
        sortKeyPretty = 'Vessel Name'
    elif sortKeyFromUser == 'length':
        sortKeyPretty = 'Length'
    elif sortKeyFromUser == 'gearType':
        sortKeyPretty = 'Gear Type'
    elif sortKeyFromUser == 'flag':
        sortKeyPretty = 'Flag'

    return render_template("results.html", results=results, gearTypeFromUser=gearTypeFromUser,
                           vesselNameFromUser=vesselNameFromUser, maxLengthFromUser=maxLengthFromUser,
                           minLengthFromUser=minLengthFromUser, flagFromUser=flagFromUser,
                           sortKeyFromUser=sortKeyPretty)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
