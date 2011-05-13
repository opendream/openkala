# -*- coding: utf8 -*-
#  Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
import simplejson as json

from quarter.models import *
from quarter.forms import *
from api.handlers import *

def postMSG(request):
    c = RequestContext(request, {
    })
    return render_to_response('postMSG.html', c, context_instance = RequestContext(request))

def test(request):
    c = RequestContext(request, {
    })
    return render_to_response('test.html', c)

def project_page(request):
    c = RequestContext(request, {
    })
    return render_to_response('project.html', c)

def project_list(request):
    try:
        projects = Project.objects.all()
    except project.DoesNotExist:
        pass
        # TODO: Why

    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project_handler = ProjectHandler()
            project_handler.create(request)
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
    
    coreStandards = CoreStandard.objects.all().order_by('code')
    # calculate grid class
    grid = 12/standard_header_length
    grid_sum = grid * standard_header_length
    grid_topic = (12 % standard_header_length) + 3
    grid_plan = 1

    weeks = range(1, 11)
    days = Task().DAY_CHOICES 

    # Standard
    standards = CoreStandard.objects.all().order_by('id')

    return render_to_response('project_overview.html', locals(), context_instance=RequestContext(request))

def topic_overview(request, project_id, topic_id):
    try:
        project = Project.objects.get(id=project_id)
        topic = Topic.objects.get(id=topic_id)
    except topic.DoesNotExist:
        raise Http404

    plans = Plan.objects.filter(topic=topic).order_by('week')
    n_blank_plans = 10 - plans.count()

    variables = {
        'project': project,
        'topic': topic,
        'plans': plans,
        'range': range(n_blank_plans)
    }

    return render_to_response('topic_overview.html', variables, context_instance=RequestContext(request))

def plan_overview(request, project_id, week):
    try:
        plan = Plan.objects.get(id=plan_id)
    except topic.DoesNotExist:
        raise Http404

    tasks = Task.objects.filter(plan=plan).order_by('day')

    variables = {
        'project.id': project_id,
        'topic.id': topic_id,
        'plan': plan,
        'tasks' : tasks,
    }

    return render_to_response('plan_overview.html', variables, context_instance=RequestContext(request))
