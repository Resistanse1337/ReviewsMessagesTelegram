from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from .functions.utils import *


class ChatUser(models.Model):
    class Meta:
        db_table = "chat_users"
        verbose_name = 'Пользователь чата'
        verbose_name_plural = 'Пользователи чата'

    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    is_manager = models.BooleanField(default=False)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.username})"

    def to_list(self):
        return [self.username, self.first_name]


class WaitForUser(models.Model):
    class Meta:
        db_table = "waits"

    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    wait_type = models.CharField(max_length=100)


class ChatGroup(models.Model):
    class Meta:
        db_table = "chat_groups"
        verbose_name = 'Телеграм группы'
        verbose_name_plural = 'Телеграм группы'

    title = models.CharField(max_length=100, verbose_name="Название чата")
    url = models.CharField(max_length=100, verbose_name="Ссылка на чат")
    group_id = models.CharField(max_length=100, unique=True, verbose_name="ID чата")
    chat_members = models.ManyToManyField(ChatUser, related_name="chat_groups", verbose_name="Участники чата")
    chat_members_who_use_mailing = models.ManyToManyField(ChatUser, related_name="groups_to_mailing",
                                                          verbose_name="Группы для рассылки")

    def this_chat_members(self):
        return ", ".join([
            f"({p.username}, {p.first_name}, {p.last_name}, {p.user_id})" for p in self.chat_members.all()
        ])

    def last_message(self):
        return "2022.05.16 21:00"

    def __str__(self):
        return f"{self.title}, {self.url}, {self.group_id}"


class Review(models.Model):
    class Meta:
        db_table = "reviews"
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    from_tg_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    from_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)


class TelegramMessage(models.Model):
    class Meta:
        db_table = "tg_messages"
        verbose_name = 'Сообщения в группах'
        verbose_name_plural = 'Сообщения в группах'

    from_tg_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    from_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=500)
    date = models.DateTimeField(default=now)
    hours_date = models.IntegerField(default=get_hours)


class TelegramMessageProxy(TelegramMessage):
    class Meta:
        proxy = True
        verbose_name = 'Статистика сообщений по часам'
        verbose_name_plural = 'Статистика сообщений по часам'


class TelegramButton(models.Model):
    class Meta:
        db_table = "tg_buttons"
        verbose_name = 'Кнопки телеграм'
        verbose_name_plural = 'Кнопки телеграм'

    button_name = models.CharField(max_length=100, verbose_name="Название кнопки")
    clicked_count = models.IntegerField(default=0, verbose_name="Количество нажатий")
    button_answer = models.CharField(max_length=1000, verbose_name="Ответ на нажатие", default="-")
    button_group = models.CharField(max_length=100, verbose_name="Группа кнопки", default="-")
    script_name = models.CharField(max_length=100, verbose_name="Название в коде", default="-")




