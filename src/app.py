from flask import Flask
from markupsafe import escape
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient()
db = client.whereismymoney_dev

@app.route('/app/<id>', methods=['GET'])
def status(id):
    query = db.app.find_one({"export":escape(id)})
    print(query)
    if (query == None):
        return {
            "error": 500
        }
    return {
        "name": escape(query['name']),
        "status": escape(query['status'])
    }




