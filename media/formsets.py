# coding=utf-8
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.forms.models import construct_instance


class GenericInlineFormSet(BaseGenericInlineFormSet):

    def save_new(self, form, commit=True):
        kwargs = {
            self.ct_field.get_attname(): ContentType.objects.get_for_model(
                self.instance, for_concrete_model=self.for_concrete_model).pk,
            self.ct_fk_field.get_attname(): self.instance.pk,
        }
        form.instance = construct_instance(form, self.model(**kwargs))
        return form.save(commit=commit)
