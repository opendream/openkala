from django.contrib import admin
from django.db import models


class Project(models.Model):
    name    = models.CharField(max_length=255)
    grade   = models.IntegerField()
    year    = models.IntegerField()
    quarter = models.IntegerField()

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title   = models.CharField(max_length=255)
    body    = models.TextField()
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.title

class Plan(models.Model):
    week         = models.IntegerField()
    goal         = models.TextField()
    activity     = models.TextField()
    sub_topic    = models.TextField()
    key_thinking = models.TextField()
    performance  = models.TextField()
    topic        = models.ForeignKey(Topic)

    def __unicode__(self):
        return 'Plan of ' + self.topic.title + ' week ' + str(self.week)

class Task(models.Model):
    DAY_CHOICES = (
        (0, 'Sun'),
        (1, 'Mon'),
        (2, 'Tue'),
        (3, 'Wed'),
        (4, 'Thu'),
        (5, 'Fri'),
        (6, 'Sat'),
    )

    day        = models.IntegerField(choices=DAY_CHOICES)
    activity   = models.TextField()
    source     = models.TextField()
    work       = models.TextField()
    assessment = models.TextField()
    plan       = models.ForeignKey(Plan)

    def __unicode__(self):
        return 'Task of ' + self.plan.__unicode__() + ' day ' + str(self.day)
