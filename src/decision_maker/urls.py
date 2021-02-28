from django.urls import path

from decision_maker.views.screener import ScreenerCreate

urlpatterns = [path("", ScreenerCreate.as_view())]
