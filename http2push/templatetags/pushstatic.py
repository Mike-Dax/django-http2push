from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from http2push.constants import lookup_extension

import os

register = template.Library()


@register.simple_tag(name='pushstatic', takes_context=True)
def pushstatic(context, path):
    url = static(path)

    request = context['request']

    link_entries = request.META.get('link_entries', [])

    filename, file_extension = os.path.splitext(path)
    typ = lookup_extension[file_extension]
    link_entries.append([url, typ])

    request.META['link_entries'] = link_entries # We'll grab this in the view right at the end

    return url