import os
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.conf import settings

from random import choice, randint

from .models import *
from .functions.db import *


logger = logging.getLogger(__name__)


@api_view(["GET"])
@csrf_protect
def reviews_index(request):
    return render(
        request,
        "new_reviews.html",
        context={
            "from_user_chat_id": request.GET.get("from_user_chat_id"),
            "username": request.GET.get("username"),
            "first_name": request.GET.get("first_name"),
            "last_name": request.GET.get("last_name"),
            "from_chat_title": request.GET.get("from_chat_title"),
            "from_chat_url": request.GET.get("from_chat_url"),
            "group_id": request.GET.get("group_id"),
        }
    )


def test_view(request):
    return render(request, "new_reviews.html")


