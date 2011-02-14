import redis

from django.db import models


class TwitterSearchTerm(models.Model):
    term = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return self.term
    
    def save(self, *args, **kwargs):
        # @@@ redis connection needs to be centralized
        db = redis.Redis(host="localhost", port=6379, db=0)
        db.zadd("twitter:search", self.term, 0)
        super(TwitterSearchTerm, self).save(*args, **kwargs)
