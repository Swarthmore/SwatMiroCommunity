"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from django.conf import settings

def swatcontext(request):
    "Returns context variables helpful for swarthmore's workflow."
    return {
            'authmethod': settings.AUTH_METHOD,
            'authnextpage': settings.CAS_REDIRECT_URL,
    }

