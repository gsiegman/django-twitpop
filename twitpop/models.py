import redis

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class TwitterSearchTerm(models.Model):
    term = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return self.term
    
    def save(self, *args, **kwargs):
        # @@@ redis connection needs to be centralized
        db = redis.Redis(host="localhost", port=6379, db=0)
        db.zadd("twitter:search", self.term, 0)
        super(TwitterSearchTerm, self).save(*args, **kwargs)


@receiver(post_delete, sender=TwitterSearchTerm)
def delete_term_from_redis(sender, instance, **kwargs):
    db = redis.Redis(host="localhost", port=6379, db=0)
    db.zrem("twitter:search", instance.term)
