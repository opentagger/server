import json
import validators
import re
from flask import Flask, request
from flask_redis import FlaskRedis

app = Flask(__name__)

user_regex = re.compile(r"https?:\/\/(?:.*\.)?reddit.com\/u(?:ser)?\/(.*)")

REDIS_URL = "redis://:@redis:6379/0"

redis_client = FlaskRedis(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bulk_users')
def get_bulk_users():
    """
    Bulk request users.

    Returns a response formatted like this:

    {
        "status": "Success",
        "username": "mostprominentsub",
        "username2": "mostprominentsub",
        "username3": null
    }

    If a username has a value of null, then there is no subreddit that we've been tracking they're in.

    Most prominent subreddit is determined by total amount of tracked comments. Users that don't meet the BARRIER environment variable are removed.
    """
    usernames = request.args.getlist("usernames")
    if usernames:
        results = {"status": "Success"}
        for item in usernames:
            resp = redis_client.get(item)
            if resp:
                pass
        return results
    else:
        return {"status": "Failure", "message": "You need to supply the usernames parameter."}