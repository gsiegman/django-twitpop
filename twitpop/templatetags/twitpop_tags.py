import redis

from django import template


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
    
    return {"tweet_cloud": tweet_cloud}
    