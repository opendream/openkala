# -*- coding: utf8 -*-
from django.contrib import admin
from django.db import models

class CoreStandard(models.Model):
    code = models.CharField(max_length=6)
    group_code = models.CharField(max_length=1)
    description = models.TextField()

    def __unicode__(self):
        return self.code

class StandardHeader(models.Model):
    title  = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.title

class Project(models.Model):
    name          = models.CharField(max_length=255)
    grade         = models.IntegerField()
    year          = models.IntegerField()
    quarter       = models.IntegerField()

    # Denormalization
    standard_header1 = models.ForeignKey(StandardHeader, related_name='standard_header1', null=True, blank=True)
    standard_header2 = models.ForeignKey(StandardHeader, related_name='standard_header2', null=True, blank=True)
    standard_header3 = models.ForeignKey(StandardHeader, related_name='standard_header3', null=True, blank=True)
    standard_header4 = models.ForeignKey(StandardHeader, related_name='standard_header4', null=True, blank=True)
    standard_header5 = models.ForeignKey(StandardHeader, related_name='standard_header5', null=True, blank=True)

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title   = models.CharField(max_length=255, null=True, blank=True)
    body    = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project)

    # Denormalization
    standard1    = models.TextField(null=True, blank=True)
    standard2    = models.TextField(null=True, blank=True)
    standard3    = models.TextField(null=True, blank=True)
    standard4    = models.TextField(null=True, blank=True)
    standard5    = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Plan(models.Model):
    week         = models.IntegerField()
    goal         = models.TextField(null=True, blank=True)
    activity     = models.TextField(null=True, blank=True)
    sub_topic    = models.TextField(null=True, blank=True)
    key_thinking = models.TextField(null=True, blank=True)
    performance  = models.TextField(null=True, blank=True)
    project      = models.ForeignKey(Project)
    topic        = models.ForeignKey(Topic, null=True, blank=True)

    def __unicode__(self):
        return 'Plan of ' + self.project.name + ' week ' + str(self.week)

class Task(models.Model):
    DAY_CHOICES = (
        (1, 'จันทร์'),
        (2, 'อังคาร'),
        (3, 'พุธ'),
        (4, 'พฤหัสบดี'),
        (5, 'ศุกร์'),
    )

    day        = models.IntegerField(choices=DAY_CHOICES, null=True, blank=True)
    hour       = models.IntegerField(null=True, blank=True)
    activity   = models.TextField(null=True, blank=True)
    source     = models.TextField(null=True, blank=True)
    work       = models.TextField(null=True, blank=True)
    assessment = models.TextField(null=True, blank=True)
    plan       = models.ForeignKey(Plan)

    def __unicode__(self):
        return 'Task of ' + self.plan.__unicode__() + ' day ' + str(self.day)
      
    def get_day_string(self):
        return self.DAY_CHOICES[self.day][1]
        
