# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
import simplejson as json

from openkala.quarter.models import *

def project_list(request):
    if request.method == 'GET':
        results = [
            {
                'id': 1,
                'name': 'project-1<b>xxx</b><br/>hi<br/>xxxxxxxxxxxxxxxxxxxx<br/>yyyyyyyyyyy',
                'grade': 6,
                'quarter': 1,
                'year': 2554
            }
        ]
    elif request.method == 'POST':
        print "post"
        print request.raw_post_data
        project = json.loads(request.raw_post_data)
        results = project

    return HttpResponse(json.dumps(results), content_type="application/json")

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

    return render_to_response('project_overview.html', variables)
