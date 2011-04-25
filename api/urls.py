from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource
from api.handlers import ProjectHandler

project_handler = Resource(ProjectHandler)
urlpatterns = patterns('',
   url(r'^projects/(?P<id>[^/]+)$', project_handler, { 'emitter_format': 'json' }),
   url(r'^projects/$', project_handler, { 'emitter_format': 'json' }),
)