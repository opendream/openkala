# -*- coding: utf8 -*-
#  Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic.list_detail import object_list, object_detail

import simplejson as json

from quarter.models import *
from quarter.forms import *
from api.handlers import *
from stockphoto.models import *

def project_getmode_helper(request, project_id):
    if not request.user.is_authenticated():
        return 'view'
    try:
        project_user_mode = ProjectUserMode.objects.get(user=request.user, project__id=project_id)
        return project_user_mode.mode
    except:
        return 'view'

def project_getmode(request, project_id):
    return HttpResponse(project_getmode_helper(request, project_id))

def project_setmode(request, project_id, mode):
    if not request.user.is_authenticated():
        return HttpResponse('view')

    project, created = ProjectUserMode.objects.get_or_create(project=Project.objects.get(id=project_id), user=User.objects.get(id=request.user.id))
    project.mode = mode
    project.save()
    return HttpResponse(project.mode)


def home(request):
    return project_list(request)

def project_list(request):
    try:
        projects = Project.objects.all()
    except project.DoesNotExist:
        pass
        # TODO: Why

    standard_headers = StandardHeader.objects.exclude(title=None).order_by('title')

    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            if request.POST.get('cancel'):
                pass
            else:
                project_handler = ProjectHandler()
                project_handler.create(request)
                messages.success(request, u'โครงงาน %s ได้ถูกสร้างแล้ว' % request.POST.get('name'))
                if request.POST.get('save'):
                    return HttpResponseRedirect('/projects#project-tab')

    else:
        form = ProjectCreateForm()
    
    return render_to_response('projects.html', locals(), context_instance=RequestContext(request))

def project_overview(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except project.DoesNotExist:
        raise Http404

    topics = Topic.objects.filter(project=project).order_by('id')
    plans = Plan.objects.filter(project=project).order_by('week')

    standard_header = []
    standard_index = []
    for i in range(8):
        sh = getattr(project, 'standard_header' + str(i + 1))
        if sh: 
            standard_header.append(sh)
            standard_index.append((i + 1, 'standard' + str(i + 1)))

    standard_header_length = len(standard_header)
    
    # calculate grid class
    grid = 12/standard_header_length
    grid_sum = grid * standard_header_length
    grid_topic = (12 % standard_header_length) + 3
    grid_plan = 1

    weeks = range(1, 11)
    days = Task().DAY_CHOICES 

    # Standard
    standards = CoreStandard.objects.all().order_by('group_code', 'code', 'id')

    # Standard
    blogs = Blog.objects.all().order_by('-created')

    # History
    histories = ProjectHistory.objects.filter(project=project).order_by('-datetime')[0:10]
    for hist in histories:
        try:
            hist.before = hist.get_previous_by_datetime(project=project)
        except :
            hist.before = hist
            hist.is_last = True

    history_last_id = hist.id if histories.count() else 0

    is_end = not bool(ProjectHistory.objects.filter(project=project, id__lt=history_last_id).count())

    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    return render_to_response('project_overview.html', locals(), context_instance=RequestContext(request))

def plan_overview(request, project_id, plan_week):
    return project_overview(request, project_id)

def blog_list(request, project_id):
    if not request.GET.get('ajax'):
        return project_overview(request, project_id)

    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    return object_list(
        request,
        Blog.objects.filter(project__id=project_id),
        template_object_name='blog',
        template_name='blog_list.html',
        paginate_by=15,
        extra_context={'project_id': project_id, 'is_view_mode': is_view_mode}
    )

def blog_detail(request, project_id, blog_id):
    if not request.GET.get('ajax'):
        return project_overview(request, project_id)

    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    return object_detail(
        request,
        Blog.objects.all(),
        object_id=blog_id,
        template_object_name='blog',
        template_name='blog_detail.html',
        extra_context={'project_id': project_id, 'blog_full': True, 'is_view_mode': is_view_mode}
    )
