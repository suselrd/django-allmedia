# coding=utf-8
# TODO the media form must check that only one media item is set as the cover for an specific album
import json
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.util import ErrorList
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import ugettext_lazy as _
from . import settings
from .validators import FileFieldValidator
from .decorators import ajax_file_upload
from .models import Media, MediaAlbum, Image, Video, MediaTag, Attachment, AjaxFileUploaded


class MediaForm(forms.ModelForm):
    """
    Form to add a media object
    """
    is_private = forms.NullBooleanField(widget=forms.CheckboxInput(), label=_(u"Private"))

    class Meta:
        model = Media
        fields = ('caption', 'private_media', 'tags',)


class MediaAlbumForm(forms.ModelForm):
    """
    Form to add a media album
    """
    class Meta:
        model = MediaAlbum
        fields = ('name', 'location', 'private_album')


class ImageForm(forms.ModelForm):
    """
    Form to add an image
    """
    default_tags = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super(ImageForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                        empty_permitted, instance)
        if instance is not None:
            self.fields['default_tags'].initial = json.dumps([{'id': obj['id'], 'text': obj['name']}
                                                              for obj in instance.tags.values('id', 'name')])
        self.fields['image'].widget.template_with_initial = '%(input)s'

    class Meta:
        model = Image
        fields = ('caption', 'private_media', 'image', 'tags')
        widgets = {'tags': forms.TextInput()}

    def full_clean(self):
        """
        For bound forms, convert tags data to list (if not list yet)
        """
        if self.is_bound:
            field_name = self.add_prefix('tags')
            try:
                data = self.data[field_name]
                if not isinstance(data, list) and data:
                    data = data.split(',')
                    self.data[field_name] = [self._get_or_create_tag(tag) for tag in data]
            except MultiValueDictKeyError:
                pass
        return super(ImageForm, self).full_clean()

    def _get_or_create_tag(self, tag):
        """
        Returns id of an existent or new-created tag
        """
        try:
            return int(tag)
        except ValueError as e:
            return MediaTag.on_site.get_or_create(name=tag)[0].pk


@ajax_file_upload(form_file_field_name="image", content_type="image")
class ImageAjaxUploadForm(ImageForm):
    pass


class VideoForm(forms.ModelForm):
    """
    Form to add a video
    """
    default_tags = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Video
        fields = ('caption', 'private_media', 'tags', 'video',)
        widgets = {'tags': forms.TextInput()}

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super(VideoForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                        empty_permitted, instance)
        if instance is not None:
            self.fields['default_tags'].initial = json.dumps([{'id': obj['id'], 'text': obj['name']}
                                                              for obj in instance.tags.values('id', 'name')])

        self.fields['video'].widget.template_with_initial = '%(input)s'

    def full_clean(self):
        """
        For bound forms, convert tags data to list (if not list yet)
        """
        if self.is_bound:
            field_name = self.add_prefix('tags')
            try:
                data = self.data[field_name]
                if not isinstance(data, list) and data:
                    data = data.split(',')
                    self.data[field_name] = [self._get_or_create_tag(tag) for tag in data]
            except MultiValueDictKeyError:
                pass
        return super(VideoForm, self).full_clean()

    def _get_or_create_tag(self, tag):
        """
        Returns id of an existent or new-created tag
        """
        try:
            return int(tag)
        except ValueError as e:
            return MediaTag.on_site.get_or_create(name=tag)[0].pk


@ajax_file_upload(form_file_field_name="video", content_type="video")
class VideoAjaxUploadForm(VideoForm):
    pass


class TagForm(forms.ModelForm):
    """
    Form to add a media tag
    """
    class Meta:
        model = MediaTag
        fields = ('name',)


@ajax_file_upload(form_file_field_name="attachment_file", content_type="all")
class AttachmentForm(forms.ModelForm):
    attachment_file = forms.FileField(label=_('Upload attachment'))

    class Meta:
        model = Attachment
        fields = ('attachment_file',)

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.id
        super(AttachmentForm, self).save(*args, **kwargs)


class AjaxFileUploadedForm(forms.ModelForm):

    class Meta:
        model = AjaxFileUploaded
        fields = ('file',)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, content="all"):
        super(AjaxFileUploadedForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                                   empty_permitted, instance)
        # setting file validators
        self.fields['file'].validators.append(FileFieldValidator(
            mime_types=settings.MEDIA_STATICFILES_FORMATS[content]['types'],
            max_size=settings.MEDIA_STATICFILES_FORMATS[content]['size']
        ))