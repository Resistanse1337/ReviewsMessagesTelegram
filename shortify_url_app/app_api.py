from django.http import JsonResponse
from rest_framework.decorators import api_view

from .functions.db import *


@api_view(["GET"])
def get_short_url_api(request):
    original_url = request.build_absolute_uri().split("original_url=")[1]
    short_url = get_short_url_db(original_url)

    return JsonResponse({"result": short_url})














