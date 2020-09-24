from flask import Flask
from markupsafe import escape
app = Flask("Serega")

@app.route('/status/<id>', methods=['GET'])
def status(id):
    return 'Hi %s' % escape(id)