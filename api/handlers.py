from piston.handler import BaseHandler
from piston.utils import rc
from quarter.models import Project
import simplejson as json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProjectHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST')
    model = Project
    fields = ('id', 'name', 'grade', 'year', 'quarter')
    
    def create(self, request, *args, **kwargs):
        attrs = json.loads(request.raw_post_data)
        attrs.pop('id')
        inst = self.model(**attrs)
        inst.save()
        return inst

    def update(self, request, id):
        attrs = json.loads(request.raw_post_data)
        attrs.pop('id')
        try:
            inst = self.queryset(request).get(pk=id)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        
        attrs = self.flatten_dict(request.data)
        for k,v in attrs.iteritems():
            setattr( inst, k, v )

        inst.save()
        return rc.ALL_OK
    
    def read(self, request, *args, **kwargs):
        if 'id' in kwargs:
            try:
                return self.queryset(request).get(pk=kwargs.get('id'))
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            limit = int(request.GET.get('limit'))
            projects = self.queryset(request)
            paginator = Paginator(projects, limit)
            try:
                page = int(request.GET.get('page'))
                tmp = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                tmp = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                tmp = paginator.page(paginator.num_pages)
            return tmp.object_list
