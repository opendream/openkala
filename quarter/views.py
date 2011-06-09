# -*- coding: utf8 -*-
#  Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME

import simplejson as json

from quarter.models import *
from quarter.forms import *
from api.handlers import *


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        return project_list(request)

def project_list(request):
    try:
        projects = Project.objects.all()
    except project.DoesNotExist:
        pass
        # TODO: Why

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
    for i in range(5):
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

    return render_to_response('project_overview.html', locals(), context_instance=RequestContext(request))

def standard_header_list(request):
    try:
        standard_header = StandardHeader.objects.all()
    except standard_header.DoesNotExist:
        pass
        # TODO: Why

    if request.method == 'POST':
        form = StandardHeaderCreateForm(request.POST)
        if form.is_valid():
            if request.POST.get('cancel'):
                pass
            else:
                standard_header = StandardHeader(request.POST)
                standard_header.save()
                messages.success(request, u'วิชาบูรณาการ %s ได้ถูกสร้างแล้ว' % request.POST.get('title'))
                if request.POST.get('save'):
                    return HttpResponseRedirect('/standard-headers#standard-header-tab')

    else:
        form = StandardHeaderCreateForm()
    
    return render_to_response('standard_headers.html', locals(), context_instance=RequestContext(request))

