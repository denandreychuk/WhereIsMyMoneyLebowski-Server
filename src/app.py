from flask import Flask
from markupsafe import escape
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.whereismymoney_dev

@app.route('/status/<id>', methods=['GET'])
def status(id):
    query = db.app.find({})
    for q in query:
        print(query)
    return "OK"



