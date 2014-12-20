# coding=utf-8
import json
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.views.generic import View
from .forms import AjaxFileUploadedForm
from django.utils.translation import ugettext_lazy as _


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class HandleAjaxFileUploadedView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        form = AjaxFileUploadedForm(request.POST, request.FILES)
        if form.valid():
            model = form.save()

            return self.render_to_response({
                'result': True,
                'object_pk': model.pk
            })

        return self.render_to_response({
            'result': False,
            'object_pk': force_text(_(u"A problem has occurred while trying to save the uploaded file."))
        })