==========================
Django AllMedia
==========================

All Media for Django>=1.6.1

Images, Videos, Attachments. All of them can be related to any django model instance (thought generic foreign key).
Image and Video tagging support.
Image thumbnail processing.

Changelog
=========
0.3.4
-----

Fix in 'upload-to' configuration usage for docs.


0.3.3
-----

Allowed 'upload-to' configuration for media and docs.


0.3.2
-----

Calling form method save_m2m to fix bug.
Implemented form class AttachmentAjaxUploadForm

0.3.1
-----

Allow decorated model forms to have additional kwargs (besides 'commit') if overwritten.

0.3.0
-----

Support for file validations by js and django

0.2.1
-----

Support for on demand thumbnail generation (if indicated by settings)

0.2.0
-----

Support for ajax file uploads

0.1.0
-----

PENDING...

Notes
-----

PENDING...

Usage
-----

1. Run ``python setup.py install`` to install.

2. Modify your Django settings to use ``media``:

3. Make sure you have compiled and installed PIL with support for jpeg.

4. Setup your thumbs generation process (optional)
    Example:

    In django settings:

    MEDIA_THUMBNAIL_SIZES =  {
        'usage_1': [('51x51', 'scale'), ('392x392', 'scale'), ('60x60', 'crop'), ('74x74', 'crop'), ('64x64', 'crop')],
        'usage_2': [('392x392', 'scale'), ('150x150', 'scale'), ('500x500', 'scale'), ('267x200', 'scale')],
    }

    In code:
    When u need to execute the thumbs generation, just call the create_thumbnails function (passing in the image_path and usage params).
    This may be done either in synchronous or asynchronous way (as a celery task).

5. If you want to use (Ajax Upload and File Validations), you need to use also bootstrap file input component and jQuery.
