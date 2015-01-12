# coding=utf-8
import magic
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class FileFieldValidator(object):

    def __init__(self, mime_types, max_size):
        super(FileFieldValidator, self).__init__()
        self.mime_types = mime_types
        self.max_size = max_size

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(1024), mime=True)
            if mime in self.mime_types:
                if value.size > self.max_size:
                    raise ValidationError(_("Please keep filesize under %s. Current filesize %s") % (filesizeformat(self.max_size), filesizeformat(value.size)))
            else:
                raise ValidationError(_("Filetype %s is not supported.") % mime)
        except AttributeError as e:
            raise ValidationError("This value could not be validated for file type" % value)