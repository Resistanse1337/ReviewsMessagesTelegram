from django.urls import path

from . import views
from . import app_api

urlpatterns = [
    path('', views.reviews_index, name='reviews_index'),

    path('save_review', app_api.save_review, name='save_review'),
    path('add_tg_message_api', app_api.add_tg_message_api, name='add_tg_message_api'),
    path('add_tg_button_api', app_api.add_tg_button_api, name='add_tg_button_api'),
    path('get_user_api', app_api.get_user_api, name='get_user_api'),
    path('set_group_to_mailing_api', app_api.set_group_to_mailing_api, name='set_group_to_mailing_api'),
    path("update_all_mailing_groups_api", app_api.update_all_mailing_groups_api, name='update_all_mailing_groups_api'),
    path("add_user_wait_api", app_api.add_user_wait_api, name='add_user_wait_api'),
    path('delete_all_user_waits_api', app_api.delete_all_user_waits_api, name='delete_all_user_waits_api'),
    path('get_user_wait_api', app_api.get_user_wait_api, name='get_user_wait_api'),
    path('get_mailing_groups_api', app_api.get_mailing_groups_api, name='get_mailing_groups_api'),
    path('get_file', app_api.get_file_api, name="get_file_api"),
    path('get_telegram_answers_api', app_api.get_telegram_answers_api, name='get_telegram_answers_api'),
    path('test', views.test_view)
]


