import django.utils.datastructures
from django.forms.models import model_to_dict
from django.http import FileResponse
from django.shortcuts import render
from django import forms

from .functions.reviews_filters import *
from .functions.utils import *
from .models import *


TMP_DIR = os.path.join(pathlib.Path(__file__).parent, "tmp")


class ExportToExcelAdmin(admin.ModelAdmin):
    actions = ["export_to_excel"]

    @admin.action(description="Сделать выгрузку в эксель")
    def export_to_excel(self, request, queryset):
        query_data = []

        for q in queryset:
            tmp_dict = model_to_dict(q)

            tmp_dict.update(self.make_with_attr_exc(self.get_user, q))
            tmp_dict.update(self.make_with_attr_exc(self.get_group, q))
            tmp_dict.update(self.make_with_attr_exc(lambda x: {"date": x.date}, q))
            tmp_dict.update(self.make_with_attr_exc(lambda x: {"last_message": x.last_message()}, q))

            query_data.append(tmp_dict)

        saved_path = save_to_csv(query_data, list(query_data[0].keys()))

        return FileResponse(open(saved_path, "rb"))

    def make_with_attr_exc(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except AttributeError:
            return {}

    def get_user(self, q):
        return {
            "username": q.from_tg_user.username, "first_name": q.from_tg_user.first_name,
            "last_name": q.from_tg_user.last_name, "user_id": q.from_tg_user.user_id,
            "is_manager": q.from_tg_user.is_manager
        }

    def get_group(self, q):
        return {
            "title": q.from_group.title, "group_url": q.from_group.url, "group_id": q.from_group.group_id
        }


class DisplayUserAndGroup(admin.ModelAdmin):
    @admin.display
    def username(self, obj):
        return obj.from_tg_user.username

    @admin.display
    def first_name(self, obj):
        return obj.from_tg_user.first_name

    @admin.display
    def last_name(self, obj):
        return obj.from_tg_user.last_name

    @admin.display
    def user_id(self, obj):
        return obj.from_tg_user.user_id

    @admin.display
    def is_manager(self, obj):
        return obj.from_tg_user.is_manager

    @admin.display
    def title(self, obj):
        return obj.from_group.title

    @admin.display
    def url(self, obj):
        return obj.from_group.url

    @admin.display
    def group_id(self, obj):
        return obj.from_group.group_id


@admin.register(Review)
class ReviewAdmin(DisplayUserAndGroup, ExportToExcelAdmin):
    list_display = ("text", "username", "first_name", "last_name", "user_id", "is_manager", "title", "url", "group_id",
                    "emotion", "date")


@admin.register(ChatUser)
class UserAdmin(ExportToExcelAdmin):
    list_display = ("username", "first_name", "last_name", "user_id", "is_manager")
    list_editable = ("is_manager", )


@admin.register(ChatGroup)
class ChatGroupAdmin(ExportToExcelAdmin):
    list_filter = (("title", SearchWithCheckboxesFilterChats), )
    list_display = ("title", "url", "group_id", "last_message", "list_of_users")
    search_fields = ("chat_members__username", "chat_members__first_name", "chat_members__last_name",
                     "chat_members__user_id", "title", "url")
    change_list_template = "change_list.html"

    ExportToExcelAdmin.actions.append("make_mailing")

    @admin.action(description="Сделать рассылку")
    def make_mailing(self, request, queryset):
        try:
            image_path = os.path.join(TMP_DIR, f"{time()}{randint(0, 1000)}")
            with open(image_path, "wb") as f:
                f.write(request.FILES["tg_photo"].read())
        except django.utils.datastructures.MultiValueDictKeyError:
            image_path = None

        for q in queryset:
            if q.group_id:
                text = request.POST.get("mailing").replace("\\n", "\n")
                send_message(q.group_id, text, image_path)

        return render(request, "success_mailing.html")

    def list_of_users(self, item):
        return format_html(", ".join(get_urls_for_django_admin(item.chat_members.all(), ChatUser)))

    def last_message(self, item):
        return get_last_message_date_from_group(item)

    list_of_users.allow_tags = True


@admin.register(TelegramMessage)
class TelegramMessageGroupAdmin(DisplayUserAndGroup, ExportToExcelAdmin):
    list_display = ("message_text", "username", "first_name", "last_name", "user_id", "title", "url", "group_id",
                    "date", "hours_date")
    list_filter = (("from_group__title", SearchWithCheckboxesFilterMessages), ("hours_date", StartTimeFilter),
                   ("from_tg_user__username", SearchWithCheckboxesFilterUsers))
    search_fields = ("from_tg_user__username", "from_tg_user__first_name", "from_tg_user__last_name",
                     "from_group__title", "from_group__url")


@admin.register(TelegramMessageProxy)
class TelegramMessageProxyGroupAdmin(DisplayUserAndGroup, ExportToExcelAdmin):
    change_list_template = 'hours_statistic.html'
    list_filter = (("hours_date", StartTimeFilter), ("from_group__title", SearchWithCheckboxesFilterMessages),
                   ("from_tg_user__username", SearchWithCheckboxesFilterUsers), )
    search_fields = ("from_tg_user__username", "from_tg_user__first_name", "from_tg_user__last_name",
                     "from_group__title", "from_group__url")
    verbose_name = 'Статистика сообщений по часам'

    def __init__(self, model, a):
        super().__init__(model, a)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        result = {}

        for item in qs:
            if result.get(item.hours_date, None) is None:
                result[item.hours_date] = {"channels": [], "users": set()}
            result[item.hours_date]["channels"].append(item.from_group.title)
            result[item.hours_date]["users"].add(item.from_tg_user.user_id)

        for k in result.keys():
            result[k]["count"] = len(result[k]["channels"])
            result[k]["channels"] = set(result[k]["channels"])
            result[k]["count_channels"] = len(result[k]["channels"])
            result[k]["users_count"] = len(result[k]["users"])

        table = []

        for k, v in result.items():
            table.append([k, v["count"], v["count_channels"], v["users_count"], v["channels"]])

        if len(table) == 0:
            return response

        table_to_save = []

        for item in table:
            table_to_save.append({"Час": item[0], "Количество сообщений": item[1],
                                  "Количество групп": item[2], "Количество пользователей": item[3],
                                  "Группы": ", ".join(item[4])})

        saved_path = save_to_csv(table_to_save, list(table_to_save[0].keys()))

        response.context_data["statistic"] = table
        response.context_data["saved_path"] = saved_path
        response.context_data["total_messages"] = TelegramMessage.objects.count()
        response.context_data["total_groups"] = ChatGroup.objects.count()
        response.context_data["total_users"] = ChatUser.objects.count()

        return response

    changelist_view.allow_tags = True


@admin.register(TelegramButton)
class TelegramButtonAdmin(ExportToExcelAdmin):
    list_display = ("button_name", "clicked_count", "button_answer", "button_group", "script_name")
    verbose_name = "Статистика нажатий телеграм кнопок"

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TelegramButtonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'button_answer':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield





