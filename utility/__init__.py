# -*- coding: utf8 -*-
from quarter.models import *
from stockphoto.models import *
from BeautifulSoup import *
from utility.dmp import diff_match_patch
from django.template.loader import render_to_string

def get_field_from_cell(project_id, cell):
    model, id, field = cell.split('-')[0:3]

    if model == '.week':
        week, model_field = cell.split(' ')
        week = int(week.split('-')[1])
        try:
            model, day, field = model_field.split('-')
        except ValueError:
            model, field = model_field.split('-')

    model = model[1:]

    if model == 'Plan':
        return getattr(Plan.objects.get(project__id=project_id, week=week), field)
    elif model == 'Task':
        return getattr(Task.objects.get(plan__project__id=project_id, plan__week=week, day=int(day)), field)
    else:
        return getattr(eval(model).objects.get(id=int(id)), field)


def prev_point_text(project_id, history_id):
    dmp = diff_match_patch()
    histories = ProjectHistory.objects.filter(project__id=project_id, id__gte=history_id).order_by('-id')

    pre = {}
    for history in histories:
        cell = history.cell
        if not pre.get(cell):
            pre[cell] = []

        pre[cell].append(dmp.patch_fromText(history.patch)[0])

    result = {}
    for cell, patches in pre.iteritems():
        result[cell] = dmp.patch_apply(patches, get_field_from_cell(project_id, cell))[0]

    return result

def get_current_text(project_id, keys):
    return dict([(cell, get_field_from_cell(project_id, cell)) for cell in keys])
    
def sanitize_html(value, valid_tags):
    valid_tags = valid_tags.split()
    valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                     if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')

def filter_html(value):
    return sanitize_html(value, 'p i strong b u a br img')

def plan_tags_form(project_id, obj, nweek):
    obj_id = obj.id
    model = obj._meta.object_name
    daymap = {1: u'จ', 2: u'อ', 3: u'พ', 4: u'พฤ', 5: u'ศ'}

    html_id = 'plan-tags-%s-%s' % (model, obj_id)

    default = {1: {}, 2: {}, 3: {}, 4:{}, 5:{}}
    for task in obj.tasks.all():
        default[task.day][task.plan.week] = 'active'


    ca = '<div id="%s"><table class="plan-tags"><thead>' % html_id
    ca += '<tr class="plan-tags-day-head"><th class="plan-tags-conner">%s</th>' % u'สัปดาห์/วัน'
    for d, day in daymap.iteritems():
        ca += '<th>%s</th>' % day
    ca += '</tr></thaed><tbody>'

    for week in range(1, nweek + 1):
        ca += '<tr class="plan-tags-week">'
        ca += '<th class="plan-tags-week"><div><a href="/projects/%s/%s/%s/weeks/%s/days/%s">%s</a></div></th>' % (project_id, model, obj_id, week, '1,2,3,4,5', week)
        for d, day in daymap.iteritems():
            ca += '<td class="plan-tags-day"><div class="%s"><a href="/projects/%s/%s/%s/weeks/%s/days/%s">%s</a></div></td>' % (default[d].get(week) or '', project_id, model, obj_id, week, d, day)
            pass
        ca += '</tr>'

    ca += '</tbody></table></div>'

    return render_to_string('plan_tags.html', {'ca': ca, 'html_id': html_id});








