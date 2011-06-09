from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource
from api.handlers import *

project_handler                  = Resource(ProjectHandler)
topic_handler                    = Resource(TopicHandler)
plan_handler                     = Resource(PlanHandler)
task_handler                     = Resource(TaskHandler)
corestandard_handler             = Resource(CoreStandardHandler)
project_plan_handler             = Resource(ProjectPlanHandler)
project_task_handler             = Resource(ProjectTaskHandler)
project_history_handler          = Resource(ProjectHistoryHandler)
project_history_get_page_handler = Resource(ProjectHistoryGetPage)

urlpatterns = patterns('',
   url(r'^projects/(?P<id>[^/]+)$', project_handler, { 'emitter_format': 'json' }),
   url(r'^projects$', project_handler, { 'emitter_format': 'json' }),
   url(r'^projects/$', project_handler, { 'emitter_format': 'json' }),
   url(r'^projects/(?P<project_id>[^/]+)/plans/(?P<week_id>[^/]+)$', project_plan_handler, { 'emitter_format': 'json' }),
   url(r'^projects/(?P<project_id>[^/]+)/tasks/(?P<week_id>[^/]+)$', project_task_handler, { 'emitter_format': 'json' }),

   url(r'^topics/(?P<id>[^/]+)$', topic_handler, { 'emitter_format': 'json' }),
   url(r'^topics$', topic_handler, { 'emitter_format': 'json' }),
   
   url(r'^plans/(?P<id>[^/]+)$', plan_handler, { 'emitter_format': 'json' }),
   url(r'^plans$', plan_handler, { 'emitter_format': 'json' }),
   
   url(r'^tasks/(?P<id>[^/]+)$', task_handler, { 'emitter_format': 'json' }),
   url(r'^tasks$', task_handler, { 'emitter_format': 'json' }),

   url(r'^corestandards/(?P<id>[^/]+)$', corestandard_handler, { 'emitter_format': 'json' }),
   url(r'^corestandards$', corestandard_handler, { 'emitter_format': 'json' }),

   url(r'^projecthistorys/getpage/(?P<project_id>[^/]+)/(?P<history_id>[^/]+)$', project_history_get_page_handler, { 'emitter_format': 'json' }, name="api_project_history_get_page"),
   url(r'^projecthistorys/(?P<project_id>[^/]+)/(?P<old_id>[^/]+)/(?P<diff_id>[^/]+)$', project_history_handler, { 'emitter_format': 'json' }, name="api_project_history"),
)
