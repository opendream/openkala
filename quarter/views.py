#  Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
import simplejson as json

from openkala.quarter.models import *

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
#    if request.method == 'GET':
#        results = [
#            {
#                'id': 1,
#                'name': 'project-1<b>xxx</b><br/>hi<br/>xxxxxxxxxxxxxxxxxxxx<br/>yyyyyyyyyyy',
#                'grade': 6,
#                'quarter': 1,
#                'year': 2554
#            }
#        ]
#    elif request.method == 'POST':
#        print "post"
#        print request.raw_post_data
#        project = json.loads(request.raw_post_data)
#        results = project
#    return HttpResponse(json.dumps(results), content_type="application/json")
    try:
        projects = Project.objects.all()
    except project.DoesNotExist:
        raise
    
    variables = {
      'projects' : projects
    }
    c = RequestContext(request, {
    })
    return render_to_response('projects.html', variables, context_instance=RequestContext(request))

def project_overview(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except project.DoesNotExist:
        raise Http404

    topics = Topic.objects.filter(project=project).order_by('title')
    n_blank_topics = 10 - topics.count()

    variables = {
        'project': project, 
        'topics': topics, 
        'range': range(n_blank_topics)
    }

    return render_to_response('project_overview.html', variables, context_instance=RequestContext(request))

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

def plan_overview(request, project_id, topic_id, plan_id):
    try:
        plan = Plan.objects.get(id=plan_id)
    except topic.DoesNotExist:
        raise Http404

    tasks = Task.objects.filter(plan=plan).order_by('day')
    n_blank_plans = 10 - plans.count()

    variables = {
        'project.id': project_id,
        'topic.id': topic_id,
        'plans': plans,
        'range': range(n_blank_plans)
    }

    return render_to_response('topic_overview.html', variables, context_instance=RequestContext(request))
