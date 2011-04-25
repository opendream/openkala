from django.contrib import admin
from django.db import models


class Project(models.Model):
    name    = models.CharField(max_length=255)
    grade   = models.IntegerField()
    year    = models.IntegerField()
    quarter = models.IntegerField()

class Topic(models.Model):
    title   = models.CharField(max_length=255)
    body    = models.TextField()
    project = models.ForeignKey(Project)

class Plan(models.Model):
    week         = models.IntegerField()
    goal         = models.TextField()
    activity     = models.TextField()
    sub_topic    = models.TextField()
    key_thinking = models.TextField()
    performance  = models.TextField()
    topic        = models.ForeignKey(Topic)

class Task(models.Model):
    day        = models.IntegerField()
    activity   = models.TextField()
    source     = models.TextField()
    work       = models.TextField()
    assessment = models.TextField()
    plan       = models.ForeignKey(Plan)
