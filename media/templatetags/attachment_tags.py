#coding=utf-8
from django.template import Library, Node, Variable
from ..models import Attachment

register = Library()


class AttachmentsForObjectNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        context[var_name] = Attachment.on_site.for_object(obj)
        return ''


@register.tag
def attachments_for(parser, token):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument. Default context variable name is `attachments`.

    Syntax::

        {% attachments_for obj %}
        {% for att in attachments %}
            {{ att }}
        {% endfor %}

        {% attachments_for obj as "my_attachments" %}

    """

    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key) + 1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'attachments_for'),
        'var_name': next_bit_for(bits, 'as', '"attachments"'),
    }
    return AttachmentsForObjectNode(**args)