import os

import msgpack
import praw
import redis

from shared import ConfigData

def main(subreddit_list):
    config = ConfigData()
    redis_client = redis.Redis(host="redis")
    reddit = praw.Reddit(user_agent=f"Ingester by /u/{config.username}", client_id=config.client_id, client_secret=config.secret_id, username=config.username, password=config.password)

    subreddit_combo = reddit.subreddit(subreddit_list)

    for comment in subreddit_combo.stream.comments():
        process_comment(comment, redis_client)

def process_comment(comment, redis_client):
    stored_data = redis_client.get(comment.author.name)
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
    if comments_list := stored_data["comments"].get(comment.subreddit.name):
        if comment.id not in comments_list:
            comments_list.append(comment.id)
    else:
        stored_data["comments"][comment.subreddit.name] = [comment.id]
    redis_client.set(comment.author.name, msgpack.packb(stored_data))

if __name__ == "__main__":
    main(os.environ["SUBREDDITS"])