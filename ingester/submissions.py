import sys

import msgpack
import praw
import redis

from shared import ConfigData

def main(subreddit_list):
    config = ConfigData()
    subreddit_string = "+".join(subreddit_list)
    redis_client = redis.Redis(host="redis")
    reddit = praw.Reddit(user_agent=f"Ingester by /u/{config.username}", client_id=config.client_id, client_secret=config.secret_id, username=config.username, password=config.password)

    subreddit_combo = reddit.subreddit(subreddit_string)

    for submission in subreddit_combo.stream.submissions():
        process_submission(submission, redis_client)

def process_submission(submission, redis_client):
    stored_data = redis_client.get(submission.author.name)
    if stored_data:
        stored_data = msgpack.unpackb(stored_data)
    else:
        stored_data = {
            "submissions": {
                # {
                    # "subredditname": [
                        # "linkid"
                    # ]
                # }
            },
            "comments": {
                # {
                    # "subredditname": [
                        # "linkid"
                    # ]
                # }
            }
        }
    if submissions_list := stored_data["submissions"].get(submission.subreddit.name):
        submissions_list.append(submission.id)
    else:
        stored_data["submissions"][submission.subreddit.name] = [submission.id]
    redis_client.set(submission.author.name, msgpack.packb(stored_data))

if __name__ == "__main__":
    main(sys.argv[1:]) # Slice to remove script name