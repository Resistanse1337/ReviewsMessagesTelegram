from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view

from .models import *
from .functions.db import *


@api_view(["POST"])
@csrf_protect
def save_review(request):
    add_review(
        from_user_chat_id=request.POST.get("from_user_chat_id"), username=request.POST.get("username"),
        first_name=request.POST.get("first_name"),
        last_name=request.POST.get("last_name"), emotion=request.POST.get("emotion"), text=request.POST.get("text"),
        from_chat_title=request.POST.get("from_chat_title"), from_chat_url=request.POST.get("from_chat_url"),
        group_id=request.POST.get("group_id")
    )

    return render(request, "success_reviews.html")


@api_view(["POST"])
def add_tg_message_api(request):
    add_tg_message(from_user_chat_id=request.POST.get("from_user_chat_id"), first_name=request.POST.get("first_name"),
                   group_id=request.POST.get("group_id"),
                   username=request.POST.get("username"), last_name=request.POST.get("last_name"),
                   from_chat_title=request.POST.get("from_chat_title"), from_chat_url=request.POST.get("from_chat_url"),
                   message_text=request.POST.get("message_text"))

    return JsonResponse({"result": "ok"})


@api_view(["POST"])
def add_tg_button_api(request):
    add_tg_button(button_name=request.POST.get("button_name"))

    return JsonResponse({"result": "ok"})


@api_view(["GET"])
def get_user_api(request):
    user_id = request.GET.get("user_id")

    return JsonResponse({"result": get_user(user_id)})


@api_view(["POST"])
def set_group_to_mailing_api(request):
    user_id = request.POST.get("user_id")
    group_id = request.POST.get("group_id")

    return JsonResponse({"result": set_group_to_mailing(user_id, group_id)})


@api_view(["POST"])
def update_all_mailing_groups_api(request):
    user_id = request.POST.get("user_id")
    unset = eval(request.POST.get("unset"))

    return JsonResponse({"result": update_all_mailing_groups(user_id, unset)})


@api_view(["POST"])
def add_user_wait_api(request):
    user_id = request.POST.get("user_id")
    wait_type = request.POST.get("wait_type")

    return JsonResponse({"result": add_user_wait(user_id, wait_type)})


@api_view(["POST"])
def delete_all_user_waits_api(request):
    user_id = request.POST.get("user_id")

    return JsonResponse({"result": delete_all_user_waits(user_id)})


@api_view(["GET"])
def get_user_wait_api(request):
    user_id = request.POST.get("user_id")

    return JsonResponse({"result": get_user_wait(user_id)})


@api_view(["GET"])
def get_mailing_groups_api(request):
    user_id = request.POST.get("user_id")

    return JsonResponse({"result": get_mailing_groups(user_id)})


@api_view(["GET"])
def get_file_api(request):
    file_path = request.GET.get("file_path")

    return FileResponse(open(file_path, "rb"))


@api_view(["GET"])
def get_telegram_answers_api(request):
    answers = {}
    answers_from_db = get_telegram_answers()

    for answer in answers_from_db:
        if answers.get(answer.button_group, None) is None:
            answers[answer.button_group] = []
        answers[answer.button_group].append({
            "button_name": answer.button_name,
            "button_answer": answer.button_answer,
            "script_name": answer.script_name,
        })

    return JsonResponse({"result": answers})











