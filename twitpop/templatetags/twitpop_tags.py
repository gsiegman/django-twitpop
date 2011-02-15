import redis

from django import template

from operator import itemgetter
from random import shuffle


register = template.Library()

@register.inclusion_tag("tweet_cloud.html")
def tweet_cloud():
    # @@@ Move to centralized location
    db = redis.Redis(host='localhost', port=6379, db=0)
    
    # @@@ Need to remove magic numbers and offer settings
    scores = db.zrevrange("twitter:search", 0, 14, withscores=True)
    
    # @@@ The following is absurd. Please pretend you never saw
    # this. Will be fixed shortly.
    tweet_cloud = []
    for score in scores[1:3]:
        tweet_cloud.append({"term": score[0], "rank": 5})
    for score in scores[3:5]:
        tweet_cloud.append({"term": score[0], "rank": 4})
    for score in scores[5:7]:
        tweet_cloud.append({"term": score[0], "rank": 3})
    for score in scores[7:9]:
        tweet_cloud.append({"term": score[0], "rank": 2})
    for score in scores[9:len(scores)+1]:
        tweet_cloud.append({"term": score[0], "rank": 1})
    
    sorted_tweet_cloud = sorted(tweet_cloud, key=itemgetter("term"))
    
    return {"tweet_cloud": sorted_tweet_cloud}
