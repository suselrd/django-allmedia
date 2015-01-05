# coding=utf-8
import os
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='media.generate_thumbnails')
def create_thumbnails(image_path, usage):
    from .settings import MEDIA_THUMBNAIL_SIZES
    from .utils import generate_thumbnail
    try:
        for size, method in MEDIA_THUMBNAIL_SIZES[usage]:
            generate_thumbnail(image_path, size, method)
    except KeyError as e:
        logger.exception(e)


@shared_task(name='media.create_thumbnail')
def create_thumbnail(image_path, size, method):
    from .utils import generate_thumbnail
    generate_thumbnail(image_path, size, method)


@shared_task(name='media.clean_temp_files')
def clean_temp_files():
    from .models import AjaxFileUploaded
    from datetime import datetime, timedelta
    try:
        temp_files = AjaxFileUploaded.objects.filter(date__lt=datetime.now()-timedelta(days=1))
        for temp_file in temp_files:
            os.remove(temp_file.file.path)
        temp_files.delete()
    except Exception as e:
        logger.exception(e)