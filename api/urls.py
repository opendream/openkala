from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource
from api.handlers import *

project_handler = Resource(ProjectHandler)
topic_handler   = Resource(TopicHandler)
plan_handler    = Resource(PlanHandler)
task_handler    = Resource(TaskHandler)

urlpatterns = patterns('',
   url(r'^projects/(?P<id>[^/]+)$', project_handler, { 'emitter_format': 'json' }),
   url(r'^projects/$', project_handler, { 'emitter_format': 'json' }),

   url(r'^topics/(?P<id>[^/]+)$', topic_handler, { 'emitter_format': 'json' }),
   url(r'^topics/$', topic_handler, { 'emitter_format': 'json' }),
   
   url(r'^plans/(?P<id>[^/]+)$', plan_handler, { 'emitter_format': 'json' }),
   url(r'^plans/$', plan_handler, { 'emitter_format': 'json' }),
   
   url(r'^tasks/(?P<id>[^/]+)$', task_handler, { 'emitter_format': 'json' }),
   url(r'^tasks/$', task_handler, { 'emitter_format': 'json' }),
)
