import os

import msgpack
import praw
import redis

from logzero import logger, loglevel

from shared import ConfigData

def main(subreddit_list, log_level):
    config = ConfigData()
    loglevel(log_level)
    redis_client = redis.Redis(host="redis")
    reddit = praw.Reddit(user_agent=f"Ingester by /u/{config.username}", client_id=config.client_id, client_secret=config.secret_id, username=config.username, password=config.password)

    subreddit_combo = reddit.subreddit(subreddit_list)

    for submission in subreddit_combo.stream.submissions():
        attrs = vars(submission)
        logger.debug(f"Received new submission: {attrs}")
        try:
            process_submission(submission, redis_client)
        except Exception as e:
            logger.exception(e)
            raise e

def process_submission(submission, redis_client):
    if not submission.author: # API edge case... this happens sometimes
        return

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
    if submissions_list := stored_data["submissions"].get(submission.subreddit.subreddit_name_prefixed):
        submissions_list.append(submission.id)
    else:
        stored_data["submissions"][submission.subreddit.subreddit_name_prefixed] = [submission.id]
    redis_client.set(submission.author.name, msgpack.packb(stored_data))

if __name__ == "__main__":
    main(os.environ["SUBREDDITS"], os.environ["LOGLEVEL"])