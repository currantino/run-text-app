from django.db import models


class VideoRequest(models.Model):
    msg = models.CharField(max_length=30)
