# coding=utf-8
import json
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from .forms import AjaxFileUploadedForm
from .mixins import JSONResponseMixin


class HandleAjaxFileUploadedView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            content = request.POST.get('content', "all")
            form = AjaxFileUploadedForm(request.POST, request.FILES, content=content)
            if form.is_valid():
                model = form.save()

                return self.render_to_response({
                    'result': True,
                    'object_pk': model.pk
                })

            messages = {}
            for i in xrange(len(form.errors)):
                item_error_list = form.errors.items()[i][1]
                for j in xrange(len(item_error_list)):
                    messages.update({j: force_text(item_error_list[j])})

            return self.render_to_response({
                'result': False,
                'failedMsgs': messages
            })

        except Exception as e:
            return self.render_to_response({
                'result': False,
                'failedMsgs': {1: force_text(_(u"A problem has occurred while trying to save the uploaded file."))}
            })
