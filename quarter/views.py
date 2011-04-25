# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import simplejson as json

def project_page(request):
    c = RequestContext(request, {
    })
    return render_to_response('project.html', c)

def projects(request):
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