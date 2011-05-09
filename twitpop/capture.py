import djcelery
djcelery.setup_loader()

import redis
import tweepy

from django.conf import settings
from twitpop.tasks import score_tweet

db = redis.Redis(host='localhost', port=6379, db=0)

class StreamWatcherListener(tweepy.StreamListener):
    
    def on_status(self, status):
        try:
            score_tweet.delay(status.text)
        except Exception as exception:
            pass
    
    def on_error(self, status_code):
        return True  # keep stream alive
    
    def on_timeout(self):
        pass


def main():
    username = settings.get('TWITPOP')['USERNAME']
    password = settings.get('TWITPOP')['PASSWORD']
    stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)
    
    track_list = db.zrange("twitter:search", 0, -1)
    stream.filter([], track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
