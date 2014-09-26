# coding=utf-8
import os
from .settings import MEDIA_IMAGE_EXTENSION, MEDIA_IMAGE_FORMAT, MEDIA_IMAGE_QUALITY


def thumbnail_path(path, size, method):
    """
    Returns the path for the resized image.
    """

    dir, name = os.path.split(path)
    image_name, ext = name.rsplit('.', 1)
    return os.path.join(dir, '%s_%s_%s.%s' % (image_name, method, size, MEDIA_IMAGE_EXTENSION))


def generate_thumbnail(path, size, method):
    try:
        import Image
    except ImportError:
        try:
            from PIL import Image
        except ImportError:
            raise ImportError('Cannot import the Python Image Library.')

    image = Image.open(path)

    # normalize image mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # parse size string 'WIDTHxHEIGHT'
    width, height = [int(i) for i in size.split('x')]

    # use PIL methods to edit images
    if method == 'scale':
        image.thumbnail((width, height), Image.ANTIALIAS)
        image.save(thumbnail_path(path, size, method), MEDIA_IMAGE_FORMAT, quality=MEDIA_IMAGE_QUALITY)

    elif method == 'crop':
        try:
            import ImageOps
        except ImportError:
            from PIL import ImageOps

        ImageOps.fit(
            image, (width, height), Image.ANTIALIAS
        ).save(thumbnail_path(path, size, method), MEDIA_IMAGE_FORMAT, quality=MEDIA_IMAGE_QUALITY)