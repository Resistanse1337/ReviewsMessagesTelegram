from django.db import models


class Url(models.Model):
    original_url = models.CharField(max_length=300)
    short_version = models.CharField(max_length=300)

    class Meta:
        db_table = "short_urls"









