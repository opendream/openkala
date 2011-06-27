from piston.handler import BaseHandler
from piston.utils import rc, Mimer

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.template.loader import render_to_string

import simplejson as json
import urllib

from quarter.models import *
from stockphoto.models import *
from utility.dmp import diff_match_patch
import utility

def urlencoded(raw):
    first = [urllib.unquote_plus(part) for part in raw.split('&')]
    second = []
    for part in first:
        sp = part.split('=')
        second.append([sp[0], '='.join(sp[1:])])
           
    return dict(second)

Mimer.register(urlencoded, ('application/x-www-form-urlencoded; charset=UTF-8',))

def insertProjectHistory(project, cell, new_value, model, id, field, user): 
    current_value = getattr(model.objects.get(id=id), field)

    if current_value == None:
        current_value = ''
    elif type(current_value) == int:
        current_value = str(current_value)

    #new_value = str(new_value)
    #new_value = new_value.decode('utf-8')
    print current_value
    print new_value
    if new_value != current_value:
        dmp = diff_match_patch()
        patches = dmp.patch_make(new_value, current_value)
        project_history = ProjectHistory(project=project, cell=cell, patch=dmp.patch_toText(patches), user=user)
        project_history.save()
        # This is a bug
        if ProjectHistory.objects.filter(project=project).count() > 1:
            project_history.before = project_history.get_previous_by_datetime(project=project)
        else:
            project_history.before = {'id': 0}

        return render_to_string('history_item.html', {'project_id': project.id, 'history': project_history, 'is_new': True})

class ProjectPlanHandler(BaseHandler):
    allowed_methods = ('GET')
    model = Plan
    fields = ['id', 'week', 'main_point', 'goal', 'activity', 'key_thinking', 'sub_topic', 'performance', 'assessment']
    fields.append('cell')
    def read(self, request, project_id, week_id):
        obj = Plan.objects.get(project__id=project_id, week=week_id)
        return obj

class ProjectTaskHandler(BaseHandler):
    allowed_methods = ('GET')
    model = Task
    fields = ['id', 'day', 'activity', 'source', 'work', 'hour']
    fields.append('cell')
    def read(self, request, project_id, week_id):
        return Task.objects.filter(plan__week=week_id, plan__project__id=project_id)

class ApiHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST')

    def set_model(self, model):
        self.model = model

    def flatten_dict(self, dct):
        fd = {}
        for k in dct.keys():
            k = k.encode('utf8')
            try:
                if k in dct:
                    typ = type(self.model._meta.get_field(k))

                    if typ == models.IntegerField:
                        fd[k] = int(dct.get(k))
                    elif typ == models.ForeignKey:
                        parent_model = self.model._meta.get_field(k).related.parent_model
                        pk = dct.get(k)
                        if type(pk) == list and len(pk):
                            pk = pk[0]

                        if pk:
                            fd[k] = parent_model.objects.get(pk=pk)
                        else:
                            fd[k] = None
                    else:
                        val = dct.get(k)
                        if val:
                            try:
                                fd[k] = val.decode('utf-8')
                            except:
                                fd[k] = val
                        else:
                            fd[k] = None

            except models.FieldDoesNotExist:
                # TODO: Do something
                # Validate html form send argument
                pass

        return fd
    
    def create(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)
        pkfield = self.model._meta.pk.name
        
        try:
            if attrs.get(pkfield) and int(attrs.get(pkfield)):
                inst = self.model.objects.get(pk=int(attrs.get(pkfield)))
            else:
                tmp = {}
                for k, attr in attrs.iteritems():
                    if type(self.model._meta.get_field(k)) != models.ForeignKey:
                        tmp[k] = attr

                if tmp:
                    inst = self.model.objects.get(**tmp)
                else:
                    inst = self.model.objects.get(pk=0)

            inst = self.update(request, args, kwargs)
            return inst
        except self.model.DoesNotExist:
            if 'id' in attrs:
                del(attrs['id'])
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    def update(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)
        pkfield = self.model._meta.pk.name

        try:
            if attrs.get(pkfield):
                inst = self.model.objects.get(pk=attrs.get(pkfield))
            else:
                inst = self.model.objects.get(**attrs)
        except self.model.DoesNotExist:
            return rc.NOT_FOUND

        project = None
        if hasattr(inst, 'project'):
            project = inst.project
        
        histories = []
        for k,v in attrs.iteritems():
            setattr( inst, k, v )

            if k not in ('id', ) and project and request.data.get('cell'):
                history = insertProjectHistory(project, request.data.get('cell'), v, self.model, inst.id, k, request.user)
                if history:
                    histories.append(history)

        print inst.__dict__
        inst.save()
        inst.histories = histories
        return inst.__dict__
    
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

class RequestBlank(object):
    def __init__(self):
        self.data = {}

class TaskHandler(ApiHandler):
    model = Task
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

    def create(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)
        pkfield = self.model._meta.pk.name
        
        try:
            inst = self.model.objects.get(plan=attrs['plan'], day=attrs['day'])

            inst = self.update(request, args, kwargs)
            return inst
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    def update(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)

        try:
            inst = self.model.objects.get(plan=attrs['plan'], day=attrs['day'])
        except self.model.DoesNotExist:
            return rc.NOT_FOUND
        
        project = attrs['plan'].project
        histories = []

        for k,v in attrs.iteritems():
            setattr( inst, k, v )

            if k not in ('plan', 'day') and project and request.data.get('cell'):
                history = insertProjectHistory(project, request.data.get('cell'), v, self.model, inst.id, k, request.user)
                if history:
                    histories.append(history)

        inst.save()
        inst.histories = histories
        return inst.__dict__

class PlanHandler(ApiHandler):
    model = Plan
    fields = ['week', 'topic', 'goal', 'activity', 'key_thingking', 'sub_topic', 'performance']
    fields.append('cell')

    def create(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)
        pkfield = self.model._meta.pk.name
        
        try:
            if not attrs.get('id'):
                inst = self.model.objects.get(project=attrs['project'], week=attrs['week'])
            else:
                inst = self.model.objects.get(id=attrs['id'])

            inst = self.update(request, args, kwargs)
            return inst
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    def update(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.data)

        try:
            if not attrs.get('id'):
                inst = self.model.objects.get(project=attrs['project'], week=attrs['week'])
            else:
                inst = self.model.objects.get(id=attrs['id'])

        except self.model.DoesNotExist:
            return rc.NOT_FOUND
        
        histories = []
        for k,v in attrs.iteritems():
            setattr( inst, k, v )
            if k not in ('week', 'project') and attrs.get('project') and request.data.get('cell'):
                history = insertProjectHistory(attrs.get('project'), request.data.get('cell'), v, self.model, inst.id, k, request.user)
                if history:
                    histories.append(history)

        inst.save()
        inst.histories = histories
        return inst.__dict__
    
class TopicHandler(ApiHandler):
    model = Topic
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

class CoreStandardHandler(ApiHandler):
    model = CoreStandard
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

    def create(self, request, *args, **kwargs):
        inst = super(CoreStandardHandler, self).create(request, args, kwargs)
        return render_to_string('standard_item.html', {'standard': inst})

class StandardHeaderHandler(ApiHandler):
    model = StandardHeader
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

    def create(self, request, *args, **kwargs):
        inst = super(StandardHeaderHandler, self).create(request, args, kwargs)
        return render_to_string('standard_header_item.html', {'standard_header': inst})

class ProjectHandler(ApiHandler):
    model = Project
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

    def create(self, request, *args, **kwargs):
        if not hasattr(request, 'data'): 
            request.data = urlencoded(request.raw_post_data)

        attrs = self.flatten_dict(request.POST)
        
        try:
            inst = self.model.objects.get(**attrs)
            self.update(request, args, kwargs)
            return inst
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()

            # Create default plans
            for i in range(10):
                request = RequestBlank()
                request.data = {'project': inst.id, 'week': str(i+1)}
                plan_handler = PlanHandler()
                plan_handler.create(request)

            # Create default topics
            for i in range(10):
                request = RequestBlank()
                request.data = {'project': inst.id}
                topic_handler = TopicHandler()
                topic_handler.create(request)

            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

class ProjectHistoryHandler(ApiHandler):
    model = ProjectHistory
    fields = [(field.name) for field in model._meta.fields]
    def read(self, request, project_id, old_id, diff_id):

        project_id, old_id, diff_id = [int(project_id), int(old_id), int(diff_id)]
        
        dmp = diff_match_patch()

        old = utility.prev_point_text(project_id, old_id)

        if diff_id:
            diff = utility.prev_point_text(project_id, diff_id)
        else:
            diff = utility.get_current_text(project_id, old.keys())

        result = {}
        for cell, html in old.iteritems():
            if cell in diff:
                d  = dmp.diff_main(html, diff[cell])
                #dmp.diff_cleanupEfficiency(d) # Suck
                dmp.diff_cleanupSemantic(d) # Damn it
                html = dmp.diff_prettyHtml(d)
                
                # I don't know why dmp replace this char
                html = html.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&para;<br>", "\n").replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")

                result[cell] = html

        return result


class ProjectHistoryGetPage(ApiHandler):
    model = ProjectHistory
    fields = [(field.name) for field in model._meta.fields]
    def read(self, request, project_id, history_id):
        histories = ProjectHistory.objects.filter(project__id=project_id, id__lt=history_id).order_by('-datetime')[0:10]

        for hist in histories:
            try:
                hist.before = hist.get_previous_by_datetime(project__id=project_id)
            except :
                hist.before = hist
                hist.is_last = True

        history_last_id = hist.id
        is_end = not bool(ProjectHistory.objects.filter(project__id=project_id, id__lt=history_last_id).count())
        html = render_to_string('history_items.html', {'project_id': project_id, 'histories': histories, 'added': True})

        return {'list': html, 'history_last_id': history_last_id, 'is_end': is_end}

class GalleryHandler(ApiHandler):
    model = Gallery
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')

class PhotoHandler(ApiHandler):
    model = Photo
    fields = [(field.name) for field in model._meta.fields]
    fields.append('cell')
