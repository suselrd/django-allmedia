# coding=utf-8
from django.conf import settings

MEDIA_IMAGE_FORMAT = getattr(settings, 'MEDIA_IMAGE_FORMAT', 'JPEG')
MEDIA_IMAGE_EXTENSION = getattr(settings, 'MEDIA_IMAGE_FORMAT', 'jpg')
MEDIA_IMAGE_QUALITY = getattr(settings, 'MEDIA_IMAGE_FORMAT', 75)

MEDIA_THUMBNAIL_SIZES = getattr(settings, 'MEDIA_THUMBNAIL_SIZES', {})
