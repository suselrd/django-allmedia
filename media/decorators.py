# coding=utf-8
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError
from .models import AjaxFileUploaded
from .signals import pre_ajax_file_save


def ajax_file_upload(form_file_field_name="file", model_file_field_name=None, content_type="all"):

    def decorator(cls):
        from django import forms
        if not issubclass(cls, forms.ModelForm):
            raise ImproperlyConfigured("ajax_file_upload decorator is only suitable for ModelForm descendants.")

        setattr(cls, 'file_field_required', cls.base_fields.get(form_file_field_name).required)

        # Init method
        normal_init_method = getattr(cls, '__init__')

        def __init__(self, *args, **kwargs):
            normal_init_method(self, *args, **kwargs)
            # create a temporal field to save the ajax file uploaded id
            self.fields['temp_file_id'] = forms.IntegerField(
                required=False,
                widget=forms.HiddenInput(attrs={"class": "temp_file_id"})
            )
             # set target field as non required
            self.fields[form_file_field_name].required = False
            # to render an attribute with the content type
            self.fields[form_file_field_name].widget.attrs.update({"data-contentvalidation": content_type})

        setattr(cls, '__init__', __init__)

        if cls.file_field_required:
            # clean method
            normal_clean_method = getattr(cls, 'clean')

            def clean(self):
                cleaned_data = normal_clean_method(self)
                if not cleaned_data.get('temp_file_id', None) and not cleaned_data.get(form_file_field_name, None):
                    raise ValidationError(message="No file provided", code="no_file")
                return cleaned_data

            setattr(cls, 'clean', clean)

        # model save method
        normal_model_save_method = getattr(cls.Meta.model, "save")

        def model_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
            # finds if self has a temp_file attribute
            if getattr(self, "temp_file", None):
                temp_file = getattr(self, "temp_file")
                # connect with pre_ajax_file_save signal
                pre_ajax_file_save.send(self.__class__, instance=self)
                # create the new field field instance
                getattr(self, model_file_field_name if model_file_field_name else form_file_field_name).save(
                    os.path.basename(temp_file.file.path),
                    temp_file.file.file,
                    False
                )

            normal_model_save_method(self, force_insert, force_update, using, update_fields)

        setattr(cls.Meta.model, 'save', model_save)

        # save method
        normal_save_method = getattr(cls, 'save')

        def save(self, commit=True, **kwargs):
            # gets the temp_file_id
            temp_file_id = self.cleaned_data.get('temp_file_id', False)
            if temp_file_id:
                try:
                    temp_file = AjaxFileUploaded.objects.get(pk=temp_file_id)
                    instance = normal_save_method(self, commit=False, **kwargs)
                    # set a new attribute temp_file to the form instance
                    setattr(instance, "temp_file", temp_file)

                    if commit:
                        instance.save()
                        self.save_m2m()

                    return instance
                except AjaxFileUploaded.DoesNotExist:
                    return normal_save_method(self, commit, **kwargs)
                except Exception as e:
                    raise e
            else:
                return normal_save_method(self, commit, **kwargs)

        setattr(cls, 'save', save)

        return cls

    return decorator