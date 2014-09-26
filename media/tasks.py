# coding=utf-8
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