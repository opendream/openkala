"""
models.py --- models used by stockphoto

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

from django.db import models
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.models as auth
from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals

from django.db.models.signals import post_save, pre_delete
from django.utils.html import strip_tags

from datetime import datetime

import os, os.path
import Image

from quarter.models import *

# Handle settings here
try:
    STOCKPHOTO_BASE = settings.STOCKPHOTO_BASE.strip('/')
except AttributeError:
    STOCKPHOTO_BASE='stockphoto'
    
try:
    STOCKPHOTO_URL = settings.STOCKPHOTO_URL
except AttributeError:
    STOCKPHOTO_URL='/stockphoto'
if STOCKPHOTO_URL[-1] == '/':
    STOCKPHOTO_URL=STOCKPHOTO_URL[:-1]

try:
    ADMIN_URL = settings.ADMIN_URL
except AttributeError:
    ADMIN_URL='/admin'
if ADMIN_URL[-1] == '/':
    ADMIN_URL=ADMIN_URL[:-1]

# Create your models here.

class Gallery(models.Model):
    title = models.CharField(_("title"), max_length=80)
    date = models.DateField(_("publication date"), auto_now_add=True)
    created = models.ForeignKey(auth.User,
                              verbose_name=_("gallery created by")
                              )
    display_width = models.IntegerField(
        _("width to display full images"),
        default=640)
    display_height = models.IntegerField(
        _("height to display full images"),
        default=480)
    thumbnail_width = models.IntegerField(
        _("width to display thumbnails"),
        default=150)
    thumbnail_height = models.IntegerField(
        _("height to display thumbnails"),
        default=100)
    thumbnail2_width = models.IntegerField(
        _("width to display thumbnails 2"),
        default=560)
    thumbnail2_height = models.IntegerField(
        _("height to display thumbnails 2"),
        default=374)

    project = models.ForeignKey(Project)

    class Meta:
        get_latest_by = '-date'
        verbose_name_plural = _("galleries")
        ordering = ['-date',]

 
    def save(self):
        if not self.title:
            self.title = datetime.today().strftime("%d/%m/%Y")

        self.title = strip_tags(self.title)
 
        super(Gallery, self).save()

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__().encode('utf8', 'replace')

    @models.permalink
    def get_absolute_url(self):
        return ('stockphoto_gallery_detail', [str(self.id)])

    def get_admin_url(self):
        return "%s/stockphoto/gallery/%d/" % (ADMIN_URL, self.id)
    def was_published_today(self):
        return self.date.date() == datetime.date.today()

    def first(self):
        try:
            return self.photo_set.all()[0]
        except IndexError:
            return None
    def update_thumbs(self):
        for photo in self.photo_set.all():
            photo.create_disp()
            photo.create_thumb()
            photo.create_thumb2()

    def striphtml(self):
        return ['title']


class Photo(models.Model):
    # import os, os.path, Image
    image = models.ImageField(_("Photograph"),
                            upload_to= STOCKPHOTO_BASE + "/%Y/%m/%d/")
    desc = models.TextField(_("description"), blank=True)
    gallery = models.ForeignKey(Gallery)
    date = models.DateField(_("date photographed"), blank=True, null=True)
    class Meta:
        get_latest_by = 'date'
        ordering = ['-id', 'desc']

    def __unicode__(self):
        return self.desc
    def __str__(self):
        return self.__unicode__().encode('utf8', 'replace')

    def delete_thumbnails(self):
        """Remove thumbnail and display-sized images when deleting.

        This may fail if, for example, they don't exist, so it should
        fail silently.  It may not be a good idea to delete the
        original, as the user may not understand that deleting it from
        the gallery deletes it from the filesystem, so currently we
        don't do that.
        
        """
        try:
            os.unlink(self.thumbpath())
        except (IOError, OSError):
            pass
        try:
            os.unlink(self.thumb2path())
        except (IOError, OSError):
            pass
        try:
            os.unlink(self.disppath())
        except (IOError, OSError):
            pass
        # Deleting the original might be a bad thing.
        #os.unlink(self.fullpath())

    @models.permalink
    def get_absolute_url(self):
        return ('stockphoto_photo_detail', [str(self.id)])

    def get_admin_url(self):
        return "%s/stockphoto/photos/%d/" % (ADMIN_URL, self.id)

    def thumbpath(self):
        """Path to the thumbnail
        """
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        return os.path.join( settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                     "cache", "thumbs", photobase)

    def thumburl(self):
        """URL to the thumbnail
        """
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        # for windows -- to avoid urls with '\' in them
        if os.sep != '/':
            photobase = photobase.replace(os.sep, '/')
        if settings.MEDIA_URL.endswith('/'):
            return settings.MEDIA_URL + STOCKPHOTO_BASE + \
                "/cache/thumbs/" + photobase
        return settings.MEDIA_URL + '/' + STOCKPHOTO_BASE + \
            "/cache/thumbs/" + photobase
            
    def thumb2path(self):
        """Path to the thumbnail
        """
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        return os.path.join( settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                     "cache", "thumbs2", photobase)

    def thumb2url(self):
        """URL to the thumbnail
        """
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        # for windows -- to avoid urls with '\' in them
        if os.sep != '/':
            photobase = photobase.replace(os.sep, '/')
        if settings.MEDIA_URL.endswith('/'):
            return settings.MEDIA_URL + STOCKPHOTO_BASE + \
                "/cache/thumbs2/" + photobase
        return settings.MEDIA_URL + '/' + STOCKPHOTO_BASE + \
            "/cache/thumbs2/" + photobase

    def disppath(self):
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        return os.path.join( settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                         "cache", photobase)

    def dispurl(self):
        photobase = self.image.name[len(STOCKPHOTO_BASE)+1:]
        # for windows -- to avoid urls with '\' in them
        if os.sep != '/':
            photobase = photobase.replace(os.sep, '/')
        if settings.MEDIA_URL.endswith('/'):
            return settings.MEDIA_URL + STOCKPHOTO_BASE + "/cache/" \
                + photobase
        return settings.MEDIA_URL + '/' + STOCKPHOTO_BASE + \
            "/cache/" + photobase            

    def fullpath(self):
        if self.image.name.startswith('/'):
            return self.image.name
        return os.path.join(settings.MEDIA_ROOT, self.image.name)

    def fullurl(self):
        if self.image.name.startswith('/'):    
            # Shouldn't happen anymore
            return (settings.MEDIA_URL +
                    self.image.name[len(settings.MEDIA_ROOT):])
        else:
            if settings.MEDIA_URL.endswith('/'):
                return settings.MEDIA_URL + self.image.name
            return settings.MEDIA_URL + '/' + self.image.name
        

    def next(self):
        '''Return id of 'next' photo in the same gallery or None if at
        the end.'''
        # we could probably be more clever here by using the new nifty 
        # db access filters and queries, but for now, this is good enough
        photo_list = [x for x in self.gallery.photo_set.all()]
        ind = photo_list.index(self)
        if (ind +1) == len(photo_list):
            return None
        else:
            return photo_list[ind + 1]

    def prev(self):
        """Return id of 'previous' photo in the same gallery or None
        if at the beginning
        """
        photo_list = [x for x in self.gallery.photo_set.all()]
        ind = photo_list.index(self)
        if ind == 0:
            return False
        else:
            return photo_list[ind - 1]

    def full_exists(self):
        return os.path.exists( self.fullpath() )

    def disp_exists(self):
        return os.path.exists( self.disppath() )

    def thumb_exists(self):
        return os.path.exists( self.thumbpath() )

    def thumb2_exists(self):
        return os.path.exists( self.thumb2path() )

    def create_disp(self):
        im = Image.open( self.fullpath() )
        format = im.format
        # create the path for the display image
        disp_path = self.disppath()
        disp_dir = os.path.dirname(disp_path)
        if not os.path.exists(disp_dir):
            os.makedirs(disp_dir, 0775)

        # Make a copy of the image, scaled, if needed.
        im.thumbnail((self.gallery.display_width,
                      self.gallery.display_height),
                     Image.ANTIALIAS)
        im.save(disp_path, format)

    def create_thumb(self):
        im = Image.open( self.fullpath() )
        format = im.format
        # create the path for the thumbnail image
        thumb_path = self.thumbpath()
        thumb_dir = os.path.dirname(thumb_path)
        if not os.path.exists(thumb_dir):
            os.makedirs(thumb_dir, 0775)

        # Make a copy of the image, scaled, if needed.
        im.thumbnail((self.gallery.thumbnail_width,
                      self.gallery.thumbnail_height),
                     Image.ANTIALIAS)
        im.save(thumb_path, format)

    def create_thumb2(self):
        im = Image.open( self.fullpath() )
        format = im.format
        # create the path for the thumbnail image
        thumb2_path = self.thumb2path()
        thumb2_dir = os.path.dirname(thumb2_path)
        if not os.path.exists(thumb2_dir):
            os.makedirs(thumb2_dir, 0775)

        # Make a copy of the image, scaled, if needed.
        im.thumbnail((self.gallery.thumbnail2_width,
                      self.gallery.thumbnail2_height),
                     Image.ANTIALIAS)
        im.save(thumb2_path, format)

    def build_display_images(self):
        """Make thumbnail and display-sized images after saving.
        
        For some reason, this may fail on a first pass (self.image may
        be empty when this is called), but if we just let it fail
        silently, it will apparently get called again and succeed.
        """
        if self.image:
            if not self.thumb_exists():
                self.create_thumb()
            if not self.thumb2_exists():
                self.create_thumb2()
            if not self.disp_exists():
                self.create_disp()

def build_display_images(sender, instance, signal, *args, **kwargs):
    """Simple hook for save-after trigger
    """
    instance.build_display_images()
def delete_thumbnails(sender, instance, signal, *args, **kwargs):
    """Simple hook for pre-delete trigger.
    """
    instance.delete_thumbnails()

post_save.connect(build_display_images, sender=Photo)
pre_delete.connect(delete_thumbnails, sender=Photo)
