# -*- encoding: utf-8 -*-

# Signal after syncdb
from quarter.models import *
from api.handlers import ApiHandler, RequestBlank
import csv

def import_model(model, filepath):
    rows = csv.DictReader(open(filepath, 'r'))
    for attrs in rows:
        for key, val in attrs.iteritems():
            try:
                attrs[key] = int(val)
            except ValueError:
                pass

        handler = ApiHandler()
        request = RequestBlank()
        request.data = attrs

        handler.set_model(model)
        handler.create(request)

def after_syncdb(sender, **kwargs):

    """
    THIS IS DUMMY CONTENT CODE
    """
    pass

    # ORDERING IMPORTANT
    #import_model(CoreStandard,   'import/CoreStandard.csv')
    #import_model(StandardHeader, 'import/StandardHeader.csv')
    #import_model(Project,        'import/Project.csv')
    #import_model(Topic,          'import/Topic.csv')
    #import_model(Plan,           'import/Plan.csv')
    #import_model(Task,           'import/Task.csv')


from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="quarter.management")
