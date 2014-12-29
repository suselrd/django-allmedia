# coding=utf-8
import json
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.views.generic import View
from .forms import AjaxFileUploadedForm
from django.utils.translation import ugettext_lazy as _
from .mixins import JSONResponseMixin


class HandleAjaxFileUploadedView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        text_error = force_text(_(u"A problem has occurred while trying to save the uploaded file."))
        try:
            form = AjaxFileUploadedForm(request.POST, request.FILES)
            if form.is_valid():
                model = form.save()

                return self.render_to_response({
                    'result': True,
                    'object_pk': model.pk
                })

            return self.render_to_response({
                'result': False,
                'failedMsg': text_error
            })

        except Exception as e:
            return self.render_to_response({
                'result': False,
                'failedMsg': text_error
            })
