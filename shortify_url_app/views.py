from django.http import HttpResponseRedirect

from .functions.db import *


def redirect_view(request, suffix):
    return HttpResponseRedirect(get_original_url_by_suffix(suffix))








