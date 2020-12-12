from django.db import models
from django.conf import settings


class UserQuota(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quota_origin = models.IntegerField(default=20)
    quota_available = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now=True)


class Predictions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_email = models.CharField(max_length=10000)
    prediction = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now=True)
