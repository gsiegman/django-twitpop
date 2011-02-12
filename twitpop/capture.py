import redis
import tweepy

from django.conf import settings


db = redis.Redis(host='localhost', port=6379, db=0)

class StreamWatcherListener(tweepy.StreamListener):
    
    def on_status(self, status):
        try:
            db.push("tweets", status.text)
        
        except Exception as exception:
            pass
    
    def on_error(self, status_code):
        print status_code
        return True  # keep stream alive
    
    def on_timeout(self):
        pass


def main():
    username = db.get("twitter:username")
    password = db.get("twitter:password")
    stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)
    
    # @@@ This is just test data, the actual list will be pushed
    # from terms entered into the django admin.
    db.rpush("twitter:search", "egypt")
    db.rpush("twitter:search", "mubarak")
    
    track_list = db.lrange("twitter:search", 0, -1)
    
    stream.filter([], track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'