from piston.handler import BaseHandler
from piston.utils import rc

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models

import simplejson as json

from quarter.models import *

class ApiHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST')

    def flatten_dict(self, dct):
        fd = {}
        for k in dct.keys():
            k = k.encode('utf8')
            try:
                if dct.get(k):
                    typ = type(self.model._meta.get_field(k))

                    if typ == models.CharField or typ == models.TextField:
                        fd[k] = dct.get(k)
                    elif typ == models.IntegerField:
                        fd[k] = int(dct.get(k))
                    elif typ == models.ForeignKey:
                        parent_model = self.model._meta.get_field(k).related.parent_model
                        fd[k] = parent_model.objects.get(pk=int(dct.get(k)))

            except models.FieldDoesNotExist:
                # TODO: Do something
                # Validate html form send argument
                pass

        return fd
    
    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.POST)
        
        try:
            inst = self.model.objects.get(**attrs)
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    def update(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name

        try:
            inst = self.model.objects.get(pk=kwargs.get(pkfield))
        except self.model.DoesNotExist:
            return rc.NOT_FOUND
        
        attrs = json.loads(request.raw_post_data)
        attrs.pop('id')
        for k,v in attrs.iteritems():
            setattr( inst, k, v )

        inst.save()
        return rc.ALL_OK
    
    def read(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name

        if pkfield in kwargs:
            try:
                return self.model.objects.get(pk=kwargs.get(pkfield))
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
            except MultipleObjectsReturned: # should never happen, since we're using a PK
                return rc.BAD_REQUEST
        else:
            limit = request.GET.get('limit') or 0
            limit = int(limit)
            items = self.model.objects.filter(*args, **kwargs)
            if not limit:
                return items

            paginator = Paginator(items, limit)
            try:
                page = request.GET.get('page') or 1
                page = int(page)
                tmp = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                tmp = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                tmp = paginator.page(paginator.num_pages)
            return tmp.object_list

class ProjectHandler(ApiHandler):
    model = Project
    fields = [(field.name) for field in model._meta.fields]

class TopicHandler(ApiHandler):
    model = Topic
    fields = [(field.name) for field in model._meta.fields]

class PlanHandler(ApiHandler):
    model = Plan
    fields = [(field.name) for field in model._meta.fields]

class TaskHandler(ApiHandler):
    model = Task
    fields = [(field.name) for field in model._meta.fields]

