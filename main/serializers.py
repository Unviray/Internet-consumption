"""
main.serializers
================
"""

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import InternetConsumption


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class InternetConsumptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetConsumption
        fields = ['user', 'consumption_date', 'upload', 'download']

class MonthConsumptionSerializer(serializers.Serializer):
    user = UserSerializer()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    total_consumption = serializers.FloatField()
    formated_total_consumption = serializers.CharField()
