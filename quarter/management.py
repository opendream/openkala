# -*- encoding: utf-8 -*-

# Signal after syncdb
from openkala.quarter.models import *
import csv

def import_model(model, filepath):
    rows = csv.DictReader(open(filepath, 'r'))
    for attrs in rows:
        for key, val in attrs.iteritems():
            try:
                attrs[key] = int(val)
            except ValueError:
                pass

        print attrs
        obj, created = model.objects.get_or_create(**attrs)
    
def after_syncdb(sender, **kwargs):

    """
    THIS IS DUMMY CONTENT CODE
    """

    # ORDERING IMPORTANT
    import_model(CoreStandard,   'import/CoreStandard.csv')
    import_model(StandardHeader, 'import/StandardHeader.csv')
    import_model(Project,        'import/Project.csv')
    import_model(Topic,          'import/Topic.csv')
    import_model(Plan,           'import/Plan.csv')
    import_model(Task,           'import/Task.csv')


from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="openkala.quarter.management")
