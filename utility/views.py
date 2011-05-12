# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    # Write data to CSV file
    writer.writerow(headers)

    for obj in qs:
        row = []
        i = 0
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()

            if type(val) == str or type(val) == unicode:
                val = val.encode('utf-8')
            elif hasattr(val, 'id'):
                val = val.pk
                headers[i] = headers[i] + '_id'
                
            row.append(val)
            i = i + 1

        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def admin_list_export(request, model_name, app_label, queryset=None, fields=None, list_display=True):
    if not queryset:
        model = get_model(app_label, model_name)
        queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            if key not in ('ot', 'o'):
                filters[str(key)] = str(value)
        if len(filters):
            queryset = queryset.filter(**filters)
    if not fields:
        if list_display and queryset.model._meta.admin and len(queryset.model._meta.admin.list_display) > 1:
            fields = queryset.model._meta.admin.list_display
        else:
            fields = None
    return export(queryset, fields)
