# -*- coding: utf8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

from datetime import date

class CoreStandard(models.Model):
    code        = models.CharField(max_length=6)
    group_code  = models.CharField(max_length=1)
    description = models.TextField()

    def save(self):
        if self.code:
            self.group_code = self.code[0].encode('utf-8')
        else:
            self.group_code = ''

        super(CoreStandard, self).save()

    def __unicode__(self):
        return self.code

class StandardHeader(models.Model):
    title  = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.title

class Project(models.Model):
    GRADE_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),)
    YEAR_CHOICES = [(year, year) for year in range(date.today().year-7, date.today().year + 3)]
    QUARTER_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4),)

    name          = models.CharField(max_length=255, verbose_name='ชื่อโครงการ')
    grade         = models.IntegerField(verbose_name="ชั้นประถมศึกษาปีที่", choices=GRADE_CHOICES)
    year          = models.IntegerField(verbose_name="ปีการศึกษา", choices=YEAR_CHOICES)
    quarter       = models.IntegerField(verbose_name="ภาคเรียน", choices=QUARTER_CHOICES)

    # Denormalization
    standard_header1 = models.ForeignKey(StandardHeader, related_name='standard_header1', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 1")
    standard_header2 = models.ForeignKey(StandardHeader, related_name='standard_header2', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 2")
    standard_header3 = models.ForeignKey(StandardHeader, related_name='standard_header3', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 3")
    standard_header4 = models.ForeignKey(StandardHeader, related_name='standard_header4', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 4")
    standard_header5 = models.ForeignKey(StandardHeader, related_name='standard_header5', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 5")
    standard_header6 = models.ForeignKey(StandardHeader, related_name='standard_header6', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 6")
    standard_header7 = models.ForeignKey(StandardHeader, related_name='standard_header7', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 7")
    standard_header8 = models.ForeignKey(StandardHeader, related_name='standard_header8', null=True, blank=True, verbose_name="วิชาบูรณาการที่ 8")

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
    standard6    = models.TextField(null=True, blank=True)
    standard7    = models.TextField(null=True, blank=True)
    standard8    = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Plan(models.Model):
    week         = models.IntegerField()
    # optional
    main_point   = models.TextField(null=True, blank=True)
    goal         = models.TextField(null=True, blank=True)
    activity     = models.TextField(null=True, blank=True)
    # must be have
    sub_topic    = models.TextField(null=True, blank=True)
    key_thinking = models.TextField(null=True, blank=True)
    performance  = models.TextField(null=True, blank=True)
    assessment   = models.TextField(null=True, blank=True)
    # relation
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
    plan       = models.ForeignKey(Plan)

    def __unicode__(self):
        return 'Task of ' + self.plan.__unicode__() + ' day ' + str(self.day)
      
    def get_day_string(self):
        return self.DAY_CHOICES[self.day][1]
        

class ProjectHistory(models.Model):
    project  = models.ForeignKey(Project)
    user     = models.ForeignKey(User)
    cell     = models.CharField(max_length=255)
    patch    = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    data     = models.CharField(max_length=255, null=True, blank=True)
