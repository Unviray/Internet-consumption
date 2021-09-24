"""
main.views
==========
"""

from datetime import date, datetime, timedelta

from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InternetConsumption
from .serializers import (
    UserSerializer,
    InternetConsumptionSerializer,
    MonthConsumptionSerializer
)


def format_octes(size, highest_label="Go", formated=True):
    """
    Format size to an High based Octets

    Args:
        size (float): data size in Ko
        highest_label (str): ["Ko", "Mo", "Go", "To"]
    """

    power = 1024
    n = 0
    power_labels = ["Ko", "Mo", "Go", "To"]

    while size >= power:
        size /= power
        n += 1

        if highest_label == power_labels[n]:
            break

    if formated:
        return f"{round(size, 2)} {power_labels[n]}"
    return round(size, 2), power_labels[n]


class Comsumption:
    def __init__(self, user, start_date) -> None:
        self.user = user
        self.start_date = start_date
        self.end_date = start_date - timedelta(days=30)

    @property
    def total_consumption(self) -> float:
        consumptions = InternetConsumption.objects.filter(
            user=self.user
        ).filter(
            consumption_date__lte=self.start_date,
            consumption_date__gte=self.end_date,
        )

        total = 0
        for consumption in consumptions:
            total += consumption.all_load()
        return total

    @property
    def formated_total_consumption(self) -> str:
        return format_octes(self.total_consumption)


# --View--

class HomeView(View):
    template_name = 'home_page.html'

    def render(self, request, context:dict):
        return render(request, self.template_name, context)

    def get(self, request):
        users = User.objects.all().order_by("username")
        today = date.today()

        get_name = request.GET.get("name", None)
        get_date = request.GET.get("date", None)

        user_object = None
        date_object = None
        if get_name:
            try:
                user_object = User.objects.get(username=get_name)
            except User.DoesNotExist:
                pass

        if get_date:
            date_object = datetime.strptime(get_date, "%Y-%m-%d")

        if user_object and date_object:
            consumption = Comsumption(user=user_object, start_date=date_object)

            total = consumption.total_consumption
            formated_total = format_octes(total, formated=False)

        return self.render(request, locals())


# --API--

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class InternetConsumptionViewSet(viewsets.ModelViewSet):
    queryset = InternetConsumption.objects.all()
    serializer_class = InternetConsumptionSerializer


class ApiMonthConsumption(APIView):
    def get(self, request):
        data_name = request.data.get("name", None)
        data_date = request.data.get("date", None)

        # GET method overwrite body
        get_name = request.GET.get("name", data_name)
        get_date = request.GET.get("date", data_date)

        user_object = None
        date_object = None

        if get_name:
            try:
                user_object = User.objects.get(username=get_name)
            except User.DoesNotExist:
                pass

        if get_date:
            date_object = datetime.strptime(get_date, "%Y-%m-%d")

        if user_object and date_object:
            consumption = Comsumption(user=user_object, start_date=date_object)
            serializer = MonthConsumptionSerializer(consumption, context={'request': request})

            return Response(serializer.data)

        return Response({})
