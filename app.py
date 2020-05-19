import json
import validators
import re
from flask import Flask, request
app = Flask(__name__)

user_regex = re.compile(r"https?:\/\/(?:.*\.)?reddit.com\/u(?:ser)?\/(.*)")
with open("data.json", "r") as datafile:
    jdata = json.load(datafile)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bulk_users')
def get_bulk_users():
    user_urls = request.args.getlist("urls")
    if user_urls:
        results = {}
        for item in user_urls:
            if validators.url(item):
                res = user_regex.search(item)
                if res:
                    username = res.group(1)
                    info = jdata["users"].get(username.lower())
                    results[username] = info
            else:
                return {"status": "Failure", "message": "One of your submitted items was not a URL!"}
        return results
    else:
        return {"status": "Failure", "message": "You need to supply the urls parameter."}