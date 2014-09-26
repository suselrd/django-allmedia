# coding=utf-8
import os.path
from django import template
from ..utils import thumbnail_path

register = template.Library()


@register.filter
def thumb_scaled(image, size):
    """
    Template filter used to scale an image
    that will fit inside the defined area.

    Returns the url of the resized image.

    {% load image_tags %}
    {{ profile.picture|thumb_scaled:"48x48" }}
    """

    thumb = thumbnail_path(image.path, size, 'scale')
    if not os.path.exists(thumb):
        return image.url

    return thumbnail_path(image.url, size, 'scale')


@register.filter
def thumb_cropped(image, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|thumb_cropped:"48x48" }}

    """
    thumb = thumbnail_path(image.path, size, 'crop')
    if not os.path.exists(thumb):
        return image.url

    return thumbnail_path(image.url, size, 'crop')
