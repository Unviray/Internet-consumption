"""
main.urls
=========
"""


from django.urls import path
from django.urls.conf import include

from rest_framework import routers

from .views import (
    HomeView,
    UserViewSet,
    InternetConsumptionViewSet,
    ApiMonthConsumption
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'consumption', InternetConsumptionViewSet)


urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('api/month-consumption/', ApiMonthConsumption.as_view()),
    path('api/', include(router.urls)),
]
