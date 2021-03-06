from flask import Flask, request, abort
from markupsafe import escape
from pymongo import MongoClient
from bson.json_util import loads, dumps

import uuid

app = Flask("WhereIsMyMoney")
client = MongoClient()
db = client.whereismymoney_dev

@app.route('/app/<id>', methods=['GET'])
def getAppWith(id):
    query = db.app.find_one({ "export" : escape(id) })
    print(query)
    if (query == None):
        return { 'error': "not found" }, 500
    return {
        "name": escape(query['name']),
        "status": escape(query['status'])
    }


@app.route('/app/create', methods=['POST'])
def createApp():
    if (("name" in request.args == False) or len(request.args["name"]) < 4):
        return { "error" : "Bad request" }, 400
    else:
        name = escape(request.args["name"])
        if (db.app.find_one({ "name" : name }) == None):  
            id = str(uuid.uuid1())  
            query = db.app.insert({
                "name": name,
                "status": "off",
                "export": id
            })
            if query == None:
                return { "error" : "failed to create app" }, 500
            else:
                return { 
                    "status" : "success",
                    "id": id
                }, 201
        else:
            return { "error": "app already exists" }, 500

@app.route('/app/delete/<id>', methods=['PUT'])
def deleteApp(id):
    query = db.app.delete_many({ "export": escape(id) })
    if query == None:
        return { "error" : "App not found" }, 500
    else:
        return { "status" : "success" }, 200
    
    
@app.route('/app/update/<id>', methods=['POST'])
def updateApp(id):
    if ("status" in request.json != False):
        status = request.json["status"]
        if (status == "off" or status == "on"): 
            query = { "export" : escape(id) }
            values = { "$set": { "status": escape(status) } }
            db.app.update_one(query, values)    
            return { "status" : "success" }, 200
        else:
             return { "error": "invalid status" }, 500
    else: 
        return { "error": "status field doesnt exist" }, 500