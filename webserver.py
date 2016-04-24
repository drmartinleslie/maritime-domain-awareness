from flask import Flask, render_template, request
from pymongo import MongoClient
from collections import defaultdict

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
    vesselTypeFromUser = request.args.get("vesselServiceType")
    minLengthFromUser = request.args.get("minLength")
    maxLengthFromUser = request.args.get("maxLength")

    query = {}

    if vesselNameFromUser:
        query["vesselName"] = vesselNameFromUser

    if minLengthFromUser and maxLengthFromUser:
        query["length"] = {"$gt": int(minLengthFromUser), "$lt": int(maxLengthFromUser)}

    if minLengthFromUser and (not maxLengthFromUser):
        query["length"] = {"$gt": int(minLengthFromUser)}

    if maxLengthFromUser and (not minLengthFromUser):
        query["length"] = {"$lt": int(maxLengthFromUser)}

    if vesselTypeFromUser:
        query["vesselServiceType"] = vesselTypeFromUser

    results = db.vessels.find(query)
    #results = db.vessels.find({"length": {"$gt": validatedMinLengthFromUser, "$lt": validatedMaxLengthFromUser}})

    #results = db.vessels.find({"vesselName":vesselNameFromUser, "length": {"$gt": validatedMinLengthFromUser, "$lt": validatedMaxLengthFromUser}})


    return render_template("results.html",results=results, vesselTypeFromUser=vesselTypeFromUser, vesselNameFromUser=vesselNameFromUser,maxLengthFromUser=maxLengthFromUser, minLengthFromUser=minLengthFromUser)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
