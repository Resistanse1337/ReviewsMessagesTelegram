import django.utils.datastructures
from django.forms.models import model_to_dict
from django.http import FileResponse
from django.shortcuts import render
from django import forms
from django.contrib import admin

from .models import *


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("original_url", "short_version")
