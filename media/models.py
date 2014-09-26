# coding=utf-8
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _


class MediaTag(models.Model):
    name = models.CharField(max_length=100)
    site = models.ForeignKey(Site, default=settings.SITE_ID)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        unique_together = ('name', 'site')

    def __unicode__(self):
        return self.name


class Media(models.Model):
    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    caption = models.CharField(max_length=200)
    album = models.ForeignKey('MediaAlbum', verbose_name=_('album'), related_name='%(class)s_list', null=True,
                              blank=True)
    is_cover = models.BooleanField(_('album cover'), default=False)

    private_media = models.BooleanField(_(u"private"), default=False)

    tags = models.ManyToManyField(MediaTag, verbose_name=_(u"tags"), related_name="%(class)s_set", null=True,
                                  blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    site = models.ForeignKey(Site, default=settings.SITE_ID)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True
        ordering = ['caption', ]

    def __unicode__(self):
        return self.caption

    def tag_list(self, sep=", "):
        return sep.join(self.tags.all())


class Image(Media):
    """
    Represents and image.
    """
    def image_upload(self, filename):
        return 'site-%s/photos/%s/%s/%s' % (
            settings.SITE_ID,
            '%s_%s' % (self.content_object._meta.app_label,
                       self.content_object._meta.object_name.lower()),
            self.content_object.pk,
            filename)
    image = models.ImageField(verbose_name=_('file'), upload_to=image_upload)


class Video(Media):
    """
    Represents a video.
    """
    def video_upload(self, filename):
        return 'site-%s/videos/%s/%s/%s' % (
            settings.SITE_ID,
            '%s_%s' % (self.content_object._meta.app_label,
                       self.content_object._meta.object_name.lower()),
            self.content_object.pk,
            filename)

    video = models.FileField(verbose_name=_('video'), upload_to=video_upload)

    def video_name(self):
        if self.video.name:
            return self.video.name.split('/').pop()
        return ""


class MediaAlbum(models.Model):
    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    name = models.CharField(_('name'), max_length=100, blank=False, null=False)
    caption = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), null=True, blank=True)
    private_album = models.BooleanField(_(u"private"), default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    site = models.ForeignKey(Site, default=settings.SITE_ID)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        ordering = ['caption', ]

    def __unicode__(self):
        return self.name


# Set the content to Media with the same MediaAlbum content
def set_content_after_album_content(instance, **kwargs):
    if (instance.content_type_id is None) and (instance.object_pk == u''):
        album = MediaAlbum.on_site.get(pk=instance.album_id)
        instance.content_type_id = album.content_type_id
        instance.object_pk = album.object_pk

# Connecting to Image pre_save signal
pre_save.connect(set_content_after_album_content, sender=Image, dispatch_uid='set_content_after_album_content')


class AttachmentManagerMixin(object):
    def for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)


class AttachmentManager(models.Manager, AttachmentManagerMixin):
    pass


class CurrentSiteAttachmentManager(CurrentSiteManager, AttachmentManagerMixin):
    pass


class Attachment(models.Model):

    def attachment_upload(self, filename):
        return 'site-%s/attachments/%s/%s/%s' % (
            settings.SITE_ID,
            '%s_%s' % (self.content_object._meta.app_label,
                       self.content_object._meta.object_name.lower()),
            self.content_object.pk,
            filename)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name="created_attachments", verbose_name=_('creator'))
    attachment_file = models.FileField(_('attachment'), max_length=255, upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    site = models.ForeignKey(Site, default=settings.SITE_ID)

    objects = AttachmentManager()
    on_site = CurrentSiteAttachmentManager()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return '%s attached %s' % (self.creator.username, self.attachment_file.name)

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]
