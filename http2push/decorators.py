from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.staticfiles.templatetags.staticfiles import static
from .constants import lookup_extension

import os

#  @push(['css/project.css', 'js/project.js'])
def push(files_map):
    # View decorator that sets the Link header for a specific set of files.

    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)

            linkheader = ''

            for path in files_map:
                url = static(path)
                filename, file_extension = os.path.splitext(path)
                typ = lookup_extension[file_extension]
                linkheader += '<%s>; rel=preload; as=%s,' % (url, typ)

            response['Link'] = response.get('Link', '') + linkheader # Just add it on

            return response
        return inner
    return decorator


#  @pushstatic()
def pushstatic():
    # Grabs the link_entries array from the template tag and generates the link header.

    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)

            linkheader = ''

            for header_pieces in request.META.get('link_entries', []):
                linkheader += '<%s>; rel=preload; as=%s,' % (header_pieces[0], header_pieces[1]) # It's of the form [url, typ]

            response['Link'] = response.get('Link', '') + linkheader

            return response
        return inner
    return decorator