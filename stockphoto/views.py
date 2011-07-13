"""
views.py --- non-generic views used by stockphoto

This file is a part of stockphoto, a simple photogallery app for
    Django sites.

Copyright (C) 2006 Jason F. McBrayer <jmcbray-django@carcosa.net>
Copyright (C) 2006 William McVey <wamcvey@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.

"""

# Create your views here.

# django imports
from django.conf import settings
from django import forms, http, template
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

# other imports
import zipfile
import os
import stat
import shutil

from datetime import datetime
from tempfile import NamedTemporaryFile, mkdtemp
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

from quarter.views import project_overview, project_getmode_helper
from quarter.models import Project
import utility


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# Handling settings here
try:
    STOCKPHOTO_BASE = settings.STOCKPHOTO_BASE.strip('/')
except AttributeError:
    STOCKPHOTO_BASE = 'stockphoto'
    
def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    try:
        info = i._getexif()
        if not info:
            return {}
    except:
        return {}

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

# models
from models import Gallery, Photo

# views

def photo_add(request, project_id, gallery_id):
    filename =  request.META['HTTP_X_FILE_NAME']
    filesize = request.META['HTTP_X_FILE_SIZE']
    filetype = request.META['HTTP_X_FILE_TYPE']

    if filetype.split('/')[0] == 'image':
        im = SimpleUploadedFile(filename, request._raw_post_data, filetype) 
        if gallery_id:
            gallery = Gallery.objects.get(id=gallery_id)
        else:
            project = Project.objects.get(id=project_id)
            gallery = Gallery(project=project, title='', created=request.user)
            gallery.save()

        photo = Photo(image=File(im), desc=filename, gallery=gallery)
        photo.save()
    return HttpResponse('/projects/%s/stockphoto/%s' % (str(project_id), str(gallery.id)))

def gallery_list(request, project_id):
    if 'HTTP_X_FILE_NAME' in request.META:
        return photo_add(request, project_id, None)
    elif not request.GET.get('ajax'):
        return project_overview(request, project_id)
    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    return object_list(
        request, 
        Gallery.objects.filter(project__id=project_id).order_by('-id'), 
        template_object_name='gallery', 
        template_name='stockphoto/gallery_list.html',
        paginate_by=15,
        extra_context={'project_id': project_id, 'is_view_mode': is_view_mode}
    )

def gallery_add(request, project_id):
    if request.GET.get('ignore'):
        return HttpResponse('')

    project = Project.objects.get(id=project_id)
    gallery = Gallery(project=project, title='', created=request.user)
    gallery.save()
    return HttpResponse('/projects/%s/stockphoto/%s' % (str(project_id), str(gallery.id)))

def gallery_detail(request, project_id, gallery_id):
    if 'HTTP_X_FILE_NAME' in request.META:
        return photo_add(request, project_id, gallery_id)
    elif not request.GET.get('ajax'):
        return project_overview(request, project_id)
    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    plan_tags_form = utility.plan_tags_form(project_id, Gallery.objects.get(id=gallery_id), 10)

    return object_detail(
        request, 
        Gallery.objects.all(), 
        object_id=gallery_id,
        template_object_name='gallery', 
        template_name='stockphoto/gallery_detail.html',
        extra_context={'project_id': project_id, 'is_view_mode': is_view_mode, 'plan_tags_form':plan_tags_form}
    )

def photo_detail(request, project_id, photo_id):
    if not request.GET.get('ajax'):
        return project_overview(request, project_id)

    photo = Photo.objects.get(id=photo_id)
    info = get_exif(photo.fullurl()[1:])
    if info:
        dt = info.get('DateTime') or info.get('DateTimeOriginal') or info.get('DateTimeDigitized')
        if dt:
            dt = datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
        else:
            dt = None
    else:
        dt = None

    # Mode
    mode = project_getmode_helper(request, project_id)
    is_view_mode = mode == 'view'

    return object_detail(
        request, 
        Photo.objects.all(), 
        object_id=photo_id,
        template_object_name='photo', 
        template_name='stockphoto/photo_detail.html',
        extra_context={'project_id': project_id, 'datetime': dt, 'is_view_mode': is_view_mode}
    )

def photo_delete(request, project_id, photo_id):
    if not request.GET.get('ajax'):
        return project_overview(request, project_id)

    try:
        photo = Photo.objects.get(id=photo_id)
    except:
        pass
        #return HttpResponse('')
        
    gallery_id = photo.gallery.id
    photo_id = None

    if photo.next():
        photo_id = photo.next().id
    elif photo.prev():
        photo_id = photo.prev().id

    photo.delete()

    if photo_id:
        return photo_detail(request, project_id, photo_id)
    else:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.delete()
        return gallery_list(request, project_id)

class ZipFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        super(forms.FileField, self).__init__(*args, **kwargs)
    def clean(self, data, initial=None):
        super(forms.FileField, self).clean(initial or data)
        zip_file = zipfile.ZipFile(data)
        if zip_file.testzip():
           raise forms.ValidationError(self.error_messages['invalid']) 
        return data

class ImportForm(forms.Form):
        zip_file = ZipFileField(required=True)
        photographer = forms.CharField()
        date = forms.DateField(required=False)


#@permission_required('gallery.add_photo')
def import_photos(request, thegallery):
    """Import a batch of photographs uploaded by the user.

    Import a batch of photographs uploaded by the user, all with
    the same information for gallery, photographer and date.  The
    title will be set from the filename, and the description will be
    blank.  Self-respecting photographers will edit the fields for
    each photograph; this is just a way to get a bunch of photographs
    uploaded quickly.

    The photographs should be wrapped up in a zip archive.  The
    archive will be unpacked (and flattened) in a temporary directory,
    and all image files will be identified and imported into the
    gallery.  Other files in the archive will be silently ignored.

    After importing the images, the view will display a page which may
    contain the number of images imported, and a link to the gallery
    into which the images were imported.
    """
    # Check if the gallery is valid
    gallery = get_object_or_404(Gallery, pk=thegallery)
    # And that the user has permission to add photos
    if not request.user.has_perm('gallery.add_photo'):
        return http.HttpResponseForbidden("No permission to add photos")

    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # So now everything is okay
            zf = zipfile.ZipFile(request.FILES['zip_file'])
            default_date = form.cleaned_data['date']
            if not default_date:
                default_date = datetime.now()

            destdir= os.path.join(settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                                  datetime.now().strftime("%Y/%m/%d/"))
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            for filename in zf.namelist():
                if filename.endswith('/'):
                    continue
                photopath = os.path.join(destdir, os.path.basename(filename))
                data = zf.read(filename)
                info = zf.getinfo(filename)
                try:
                    date = datetime(info.date_time[0],
                                    info.date_time[1],
                                    info.date_time[2])
                except:
                    date = default_date
                file_data = StringIO(data)
                try:
                    Image.open(file_data)
                except:
                    # don't save and process non Image files
                    continue
                photo = file(photopath, "wb")
                photo.write(data)

                # Create the object
                if photopath.startswith(os.path.sep):
                    photopath = photopath[len(settings.MEDIA_ROOT):]
                photo = Photo(image=photopath, date=date,
                              photographer=form.cleaned_data['photographer'],
                              title = os.path.basename(filename),
                              gallery_id = thegallery)
                # Save it -- the thumbnails etc. get created.
                photo.save()
                
            # And jump to the directory for this gallery
            response = http.HttpResponseRedirect(reverse('stockphoto_gallery_detail',
                                               kwargs={'object_id':
                                                       str(thegallery),}))
            response['Pragma'] = 'no cache'
            response['Cache-Control'] = 'no-cache'
            return response
        else:
            return render_to_response('stockphoto/import_form.html',
                                      dict(form=form, gallery=gallery),
                                      context_instance=RequestContext(request))
            
    else:
        form = ImportForm()
        return render_to_response('stockphoto/import_form.html',
                              dict(form=form, gallery=gallery),
                              context_instance=RequestContext(request))

#@login_required
def export(request, thegallery):
    """Export a gallery to a zip file and send it to the user.
    """
    # Check if the gallery is valid
    gallery = get_object_or_404(Gallery, pk=thegallery)
    
    # gather up the photos into a new directory
    tmpdir = mkdtemp()
    for photo in gallery.photo_set.all():
        shutil.copy(photo.get_image_filename(),
                        tmpdir)
    files = [ os.path.join(tmpdir, ff) for ff in os.listdir(tmpdir) ]
    outfile = NamedTemporaryFile()
    zf = zipfile.ZipFile(outfile, "w",
                         compression=zipfile.ZIP_DEFLATED)
    for filename in files:
        zf.write(filename, arcname=os.path.basename(filename))
    zf.close()
    outfile.flush()
    outfile.seek(0)
    shutil.rmtree(tmpdir)
    response = HttpResponse(outfile)
    response['Content-Type'] = "application/zip"
    response['Content-Length'] = str(os.stat(outfile.name)[stat.ST_SIZE])
    response['Content-Disposition'] = "attachment; filename=photos.zip"
    return response

