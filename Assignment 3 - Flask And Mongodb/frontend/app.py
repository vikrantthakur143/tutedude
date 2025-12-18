from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
client = pymongo.MongoClient(MONGO_URL)
db = client.my_db
collection = db['my_collection']

app = Flask(__name__)

@app.route('/')
def home():
    dey_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', dey_of_week=dey_of_week, current_time=current_time)

@app.route('/time')
def time():
    current_time = datetime.now().strftime('%H:%M:%S')
    return current_time

@app.route('/api')
def api_home():
    return """
    <p>Welcome to Flask api!</p>
    /api/users/fetch/<name>/<age>
    </br>
    /api/users/request?name=<name>&age=<age>
    </br>

    curl 'http://127.0.0.1:5000/api/users/fetch/vikrant/36' ;echo | jq
    </br>
    curl 'http://127.0.0.1:5000/api/users/request?name=vikrant&age=36' ;echo | jq
"""



@app.route('/api/users/fetch/<name>/<age>', methods=['GET', 'POST'])
def users_fetch(name,age):
    name = str(name)
    age = int(age)
    result = {
            'name': name,
            'age': age
    }
    return result


@app.route('/api/users/request', methods=['GET', 'POST'])
def users_request():
    name = str(request.values.get('name'))
    age = int(request.values.get('age'))

    if age >= 18:
        adult = 'Yes'
    else:
        adult = 'No'

    result = {
            'name': name,
            'age': age,
            'adult': adult
    }

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

