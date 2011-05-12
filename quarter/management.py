# -*- encoding: utf-8 -*-

# Signal after syncdb
from openkala.quarter.models import *
import csv

def import_model(model, filepath):
    rows = csv.DictReader(open(filepath, 'r'))
    for attrs in rows:
        obj, created = model.objects.get_or_create(**attrs)
    
def after_syncdb(sender, **kwargs):

    """
    THIS IS DUMMY CONTENT CODE
    """

    # ORDERING IMPORTANT
    import_model(CoreStandard,   'import/corestandard.csv')
    import_model(StandardHeader, 'import/standardheader.csv')
    import_model(Project,        'import/project.csv')
    import_model(Topic,          'import/topic.csv')
    import_model(Plan,           'import/plan.csv')
    import_model(Task,           'import/task.csv')


from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="openkala.quarter.management")
