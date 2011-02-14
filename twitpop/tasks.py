import redis

from celery.task import task
from twitpop.models import TwitterSearchTerm


@task()
def score_tweet(tweet_text):
    db = redis.Redis(host='localhost', port=6379, db=0)
    search_terms = set(db.zrange("twitter:search", 0, -1))
    matches = list(search_terms.intersection(tweet_text.split()))
    
    for match in matches:
        db.zincrby("twitter:search", match, 1)
        return match
