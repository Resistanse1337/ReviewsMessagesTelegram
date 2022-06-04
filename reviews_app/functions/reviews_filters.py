from django import forms
from django.contrib import admin

from ..functions.db import *


class StartTimeFilter(admin.filters.FieldListFilter):
    template = 'hours_date.html'

    def __init__(self, *args, **kwargs):
        super(StartTimeFilter, self).__init__(*args, **kwargs)
        self.form = forms.Form()

    def expected_parameters(self):
        return ["from", "to"]

    def choices(self, cl):
        return []

    def queryset(self, request, queryset):
        from_ = request.GET.get("from")
        to = request.GET.get("to")

        if from_ is not None and to is not None:
            return get_tg_message_by_date_range(from_, to)


class SearchWithCheckboxesFilterBase(admin.AllValuesFieldListFilter):
    template = 'base_search_with_checkboxes.html'

    def __init__(self, *args, **kwargs):
        super(SearchWithCheckboxesFilterBase, self).__init__(*args, **kwargs)
        self.form = forms.Form()


class SearchWithCheckboxesFilterUsers(SearchWithCheckboxesFilterBase):
    template = 'search_with_checkboxes_users.html'

    def expected_parameters(self):
        users = [u.username for u in get_all_chat_users()] + ["Все", "All", "filter_type"]

        return users

    def queryset(self, request, queryset):
        if request.GET.get("filter_type") != "users":
            return queryset
        if request.GET.get("Все") is not None or request.GET.get("All") is not None or len(request.GET) == 0 or \
           request.GET.get("filter_type") != "users":
            return get_all_chat_telegram_messages()

        users = []

        for k, v in request.GET.items():
            if v == "ok":
                users.append(k)

        users = get_chat_users_with_filter(username__in=users)

        return get_tg_messages_with_filter(from_tg_user__in=users)


class SearchWithCheckboxesFilterChats(SearchWithCheckboxesFilterBase):
    template = 'search_with_checkboxes_chats.html'

    def expected_parameters(self):
        titles = [g.title for g in get_all_groups()] + ["Все", "All", "filter_type"]

        return titles

    def queryset(self, request, queryset):
        if request.GET.get("filter_type") != "chats":
            return queryset
        if request.GET.get("Все") is not None or request.GET.get("All") is not None or len(request.GET) == 0:
            return get_all_groups()

        titles = []

        for k, v in request.GET.items():
            if v == "ok":
                titles.append(k)

        return get_groups_with_filter(title__in=titles)


class SearchWithCheckboxesFilterMessages(SearchWithCheckboxesFilterBase):
    template = 'search_with_checkboxes_messages.html'

    def expected_parameters(self):
        groups = [g.title for g in get_all_groups()] + ["Все", "All", "filter_type"]

        return groups

    def queryset(self, request, queryset):
        if request.GET.get("filter_type") != "messages":
            return queryset
        if request.GET.get("Все") is not None or request.GET.get("All") is not None or len(request.GET) == 0:
            return get_all_chat_telegram_messages()

        groups = []

        for k, v in request.GET.items():
            if v == "ok":
                groups.append(k)

        groups = get_groups_with_filter(title__in=groups)

        return get_tg_messages_with_filter(from_group__in=groups)



