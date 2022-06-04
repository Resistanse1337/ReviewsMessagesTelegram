from .utils import *
from ..models import *
from django.core.exceptions import ObjectDoesNotExist


def suffix_exists(suffix):
    try:
        Url.objects.get(short_version=get_url(suffix))
        return True
    except ObjectDoesNotExist:
        return False


def get_short_url_db(url):
    try:
        short_url = Url.objects.get(original_url=url)
        return short_url.short_version
    except ObjectDoesNotExist:
        pass

    suffix = make_suffix()

    while suffix_exists(suffix) is True:
        suffix = make_suffix()

    url = Url(original_url=url, short_version=get_url(suffix))
    url.save()

    return url.short_version


def get_original_url_by_suffix(suffix):
    try:
        original_url = Url.objects.get(short_version=get_url(suffix))
        return original_url.original_url
    except ObjectDoesNotExist:
        pass

