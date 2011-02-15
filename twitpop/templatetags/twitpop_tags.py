import redis

from django import template

from operator import itemgetter
from random import shuffle


register = template.Library()

@register.inclusion_tag("tweet_cloud.html")
def tweet_cloud():
    # @@@ Move to centralized location
    db = redis.Redis(host='localhost', port=6379, db=0)
    scores = db.zrevrange("twitter:search", 0, 14, withscores=True)
    
    total_score = 0
    for score in scores:
        total_score += score[1]
    
    tweet_cloud = []
    for score in scores:
        if (score[1]/total_score) >= 0.2:
            rank = 5
        elif (score[1]/total_score) >= 0.15:
            rank = 4
        elif (score[1]/total_score) >= 0.10:
            rank = 3
        elif (score[1]/total_score) >= 0.05:
            rank = 2
        elif (score[1]/total_score) >= 0.00:
            rank = 1
        
        tweet_cloud.append({"term": score[0], "rank": rank})
    
    sorted_tweet_cloud = sorted(tweet_cloud, key=itemgetter("term"))
    
    return {"tweet_cloud": sorted_tweet_cloud}
    