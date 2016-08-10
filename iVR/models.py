from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import json

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='static/profile_images', blank=True, default='static/profile_images/ivr.png')

    def __unicode__(self):
        return self.user.username

class Feed(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    likesnumber = models.IntegerField(default=0)
    commentsnumber = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='static/feeds_images')

    def __unicode__(self):
        return self.content

class News(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.CharField(max_length=30)
    commentsnumber = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='static/news_images')

    class Meta:
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.title

class Device(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0)
    developer = models.CharField(max_length=30)
    score = models.FloatField(default=0)
    reviewsnumber = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    devicedescription = models.TextField()
    picture1 = models.ImageField(upload_to='static/devices_images')
    picture2 = models.ImageField(upload_to='static/devices_images')
    picture3 = models.ImageField(upload_to='static/devices_images')

    def __unicode__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    score = models.FloatField(default=0)
    reviewsnumber = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    videodescription = models.TextField()
    picture1 = models.ImageField(upload_to='static/videos_images')
    picture2 = models.ImageField(upload_to='static/videos_images')
    picture3 = models.ImageField(upload_to='static/videos_images')

    def __unicode__(self):
        return self.title

class Game(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(default=0)
    developer = models.CharField(max_length=30)
    score = models.FloatField(default=0)
    reviewsnumber = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    gamedescription = models.TextField()
    picture1 = models.ImageField(upload_to='static/games_images')
    picture2 = models.ImageField(upload_to='static/games_images')
    picture3 = models.ImageField(upload_to='static/games_images')

    def __unicode__(self):
        return self.name

class FeedLike(models.Model):
    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.feed.content

class FeedComment(models.Model):
    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=140)

    def __unicode__(self):
        return self.content

class NewsComment(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=140)

    def __unicode__(self):
        return self.content

class DeviceReview(models.Model):
    device = models.ForeignKey(Device)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    content = models.CharField(max_length=140)

    def __unicode__(self):
        return self.content

class VideoReview(models.Model):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    content = models.CharField(max_length=140)

    def __unicode__(self):
        return self.content

class GameReview(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    content = models.CharField(max_length=140)

    def __unicode__(self):
        return self.content

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follow_user')
    followeduser = models.ForeignKey(User, related_name='followed_user')
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username + " follows " + self.followeduser.username












