import djcelery
djcelery.setup_loader()

import redis
import tweetstream

from twitpop.tasks import score_tweet

db = redis.Redis(host='localhost', port=6379, db=0)


def main():
    username = db.get("twitter:username")
    password = db.get("twitter:password")
    track_list = db.zrange("twitter:search", 0, -1)
    
    with tweetstream.FilterStream(username, password, track=track_list) as stream:
        for tweet in stream:
            text = tweet["text"]

            try:
                score_tweet.delay(text)
            except Exception as exception:
                pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
