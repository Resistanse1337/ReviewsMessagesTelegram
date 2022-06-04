from django.urls import path

from . import views
from . import app_api

urlpatterns = [
    path('get_short_url_api', app_api.get_short_url_api, name='get_short_url_api'),
    path('redirect/<str:suffix>', views.redirect_view, name='redirect_view')
]


