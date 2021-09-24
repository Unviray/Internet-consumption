"""
main.admin
==========
"""

from django.contrib import admin

from .models import InternetConsumption


admin.site.register(InternetConsumption)
