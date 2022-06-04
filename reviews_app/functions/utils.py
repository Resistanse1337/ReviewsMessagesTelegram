import os
import csv
import pathlib
from time import time
from random import randint

import telebot
from datetime import datetime
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.contrib.admin.templatetags.admin_urls import admin_urlname


def get_hours():
    return int(datetime.today().strftime('%H'))


def get_urls_for_django_admin(query_set_obj, model_object):
    urls = []

    for chat in query_set_obj:
        url = resolve_url(admin_urlname(model_object._meta, 'change'), chat.id)
        url = format_html('<a href="{url}">{name}</a>'.format(url=url, name=str(chat)))

        urls.append(url)

    return urls


def send_message(to, text, photo=None):
    bot = telebot.TeleBot(settings.BOT_TOKEN)
    if photo is None:
        bot.send_message(to, text)
    else:
        bot.send_photo(to, open(photo, "rb"), caption=text)


def save_to_csv(data, fieldnames):
    tmp_path = os.path.join(pathlib.Path(__file__).parent.parent, "tmp")
    path_to_save = os.path.join(tmp_path, f'{time()}_{randint(0, 10000)}.csv')

    with open(path_to_save, 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for dt in data:
            writer.writerow(dt)

    return path_to_save


if __name__ == "__main__":
    data = [{"1": "2", "2": "3"}, {"1": "11", "2": "32131"}, {"1": "dfs", "2": "dsf"}, {"1": "4", "2": "efds"}]

    csv_path = save_to_csv(data, list(data[0].keys()))
    print(csv_path)




