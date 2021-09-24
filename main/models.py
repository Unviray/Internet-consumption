"""
main.models
===========
"""

from django.db import models
from django.contrib.auth.models import User


class InternetConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    consumption_date = models.DateTimeField()
    upload = models.FloatField()
    download = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user} {self.consumption_date}"

    def all_load(self) -> float:
        return self.upload + self.download
