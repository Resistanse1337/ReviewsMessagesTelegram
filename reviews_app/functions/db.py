from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from reviews_app.models import *
from reviews_app.functions.utils import *


def create_chat_user(username, first_name, last_name, user_id):
    return ChatUser.objects.get_or_create(user_id=user_id, defaults={
        "username": username, "first_name": first_name, "last_name": last_name
    })


def create_chat_group(title, url, group_id):
    return ChatGroup.objects.get_or_create(group_id=group_id, defaults={"title": title, "url": url})


def create_user_and_group(username, first_name, last_name, from_user_chat_id, from_chat_title, from_chat_url, group_id):
    with transaction.atomic():
        user, _ = create_chat_user(username, first_name, last_name, from_user_chat_id)
        group, _ = create_chat_group(from_chat_title, from_chat_url, group_id)

        group.chat_members.add(user)

        return user, group


def create_review(user, group, emotion, text):
    review = Review(from_tg_user=user, from_group=group, emotion=emotion, text=text)
    review.save()


def add_review(from_user_chat_id, first_name, group_id, username, last_name, from_chat_title, from_chat_url, emotion,
               text):
    with transaction.atomic():
        user, group = create_user_and_group(username, first_name, last_name, from_user_chat_id, from_chat_title,
                                            from_chat_url, group_id)
        create_review(user, group, emotion, text)


def add_tg_message(from_user_chat_id, first_name, group_id, username, last_name, from_chat_title, from_chat_url,
                   message_text):
    with transaction.atomic():
        user, group = create_user_and_group(username, first_name, last_name, from_user_chat_id, from_chat_title,
                                            from_chat_url, group_id)
        message = TelegramMessage(from_tg_user=user, from_group=group, message_text=message_text)
        message.save()


def add_review(from_user_chat_id, username, first_name, last_name, emotion, text, from_chat_title, from_chat_url,
               group_id):
    with transaction.atomic():
        user, group = create_user_and_group(username, first_name, last_name, from_user_chat_id, from_chat_title,
                                            from_chat_url, group_id)

        review = Review(from_tg_user=user, from_group=group, emotion=emotion, text=text)
        review.save()


def add_tg_button(button_name):
    with transaction.atomic():
        button, _ = TelegramButton.objects.get_or_create(button_name=button_name)
        button.clicked_count += 1
        button.save()


def get_user(user_id):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)

        result.update({"username": user.username, "first_name": user.first_name, "last_name": user.last_name,
                       "error": False, "groups": [], "groups_to_mailing": [], "is_manager": user.is_manager})

        for group in user.chat_groups.all():
            result["groups"].append((group.group_id, group.title))

        for group in user.groups_to_mailing.all():
            result["groups_to_mailing"].append((group.group_id, group.title))
    except ObjectDoesNotExist:
        pass

    return result


def set_group_to_mailing(user_id, group_id):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)
        group = ChatGroup.objects.get(group_id=group_id)

        if group not in user.groups_to_mailing.filter(group_id=group_id):
            user.groups_to_mailing.add(group)
        else:
            user.groups_to_mailing.remove(group)
        user.save()

        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def update_all_mailing_groups(user_id, unset=True):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)

        if unset is True:
            for group in user.groups_to_mailing.all():
                user.groups_to_mailing.remove(group)
        else:
            for group in user.chat_groups.all():
                user.groups_to_mailing.add(group)

        user.save()

        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def add_user_wait(user_id, wait_type):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)

        wait = WaitForUser(user=user, wait_type=wait_type)
        wait.save()

        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def delete_all_user_waits(user_id):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)
        WaitForUser.objects.filter(user=user).delete()

        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def get_user_wait(user_id):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)
        try:
            wait = WaitForUser.objects.get(user=user)
        except ObjectDoesNotExist:
            result["reason"] = "Wait does not exists"
            return result

        result["wait"] = wait.wait_type
        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def get_mailing_groups(user_id):
    result = {
        "error": True
    }

    try:
        user = ChatUser.objects.get(user_id=user_id)

        mailing_groups = []

        for mg in user.groups_to_mailing.all():
            mailing_groups.append(mg.group_id)

        result["mailing_groups"] = mailing_groups
        result["error"] = False
    except ObjectDoesNotExist:
        pass

    return result


def get_tg_message_by_date_range(from_, to):
    return TelegramMessage.objects.filter(date__range=(from_, to))


def get_all_chat_users():
    return ChatUser.objects.all()


def get_all_chat_telegram_messages():
    return TelegramMessage.objects.all()


def get_chat_users_with_filter(**filters):
    return ChatUser.objects.filter(**filters)


def get_tg_messages_with_filter(**filters):
    return TelegramMessage.objects.filter(**filters)


def get_last_message_date_from_group(group):
    return TelegramMessage.objects.filter(from_group=group).latest("date").date


def get_all_groups():
    return ChatGroup.objects.all()


def get_groups_with_filter(**filters):
    return ChatGroup.objects.filter(**filters)


def get_telegram_answers():
    return TelegramButton.objects.all()


