from piston.handler import BaseHandler
from piston.utils import rc

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import simplejson as json

from quarter.models import *

class ApiHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST')
    model = None
    
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
            inst = self.queryset(request).get(pk=kwargs.get(pkfield))
        except self.model.DoesNotExist:
            return rc.NOT_FOUND
        
        attrs = self.flatten_dict(request.POST)
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

