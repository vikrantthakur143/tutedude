from flask import Flask, request
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URL_ENV = os.getenv('MONGO_URL')
client = pymongo.MongoClient(MONGO_URL_ENV)
db = client.my_db
collection = db['my_collection']

app = Flask(__name__)

@app.route('/api/submit', methods=['POST'])
def submit():
#    name = request.form.get('name')
    form_data = dict(request.form)
    collection.insert_one(form_data)
    return 'Data Submitted Successfully.'

@app.route('/api/view')
def view():
    data = collection.find()
    data = list(data)
    for item in data:
        print(item)
        del item['_id']
    data = {
        'data': data
    }
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
