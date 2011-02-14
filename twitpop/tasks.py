import redis

from celery.task import task
from twitpop.models import TwitterSearchTerm


@task()
def score_tweet(tweet_text):
    # @@@ this should be cached, no need to query db every time
    search_terms = set(TwitterSearchTerm.objects.values_list("term", flat=True))
    matches = list(search_terms.intersection(tweet_text.split()))
    
    # @@@ there has to be a better way to manage this connection
    db = redis.Redis(host='localhost', port=6379, db=0)
    
    for match in matches:
        db.zincrby("twitter:search", match, 1)
        return match
