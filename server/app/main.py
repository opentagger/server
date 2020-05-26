import json
import msgpack
import validators
import re
from flask import Flask, request
from flask_redis import FlaskRedis

app = Flask(__name__)

user_regex = re.compile(r"https?:\/\/(?:.*\.)?reddit.com\/u(?:ser)?\/(.*)")

app.config["REDIS_URL"] = "redis://:@redis:6379/0"

redis_client = FlaskRedis(app)

def add_item_count_to_dict(d, item):
    if item not in d:
        d[item] = 0
    d[item] += 1


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
                known_data = msgpack.unpackb(resp)
                subs_dict = {}

                for subredditname in known_data["submissions"]:
                    add_item_count_to_dict(subs_dict, subredditname)
                for subredditname in known_data["comments"]:
                    add_item_count_to_dict(subs_dict, subredditname)

                results[item] = max(subs_dict, key=subs_dict.get)
        return results
    else:
        return {"status": "Failure", "message": "You need to supply the usernames parameter."}