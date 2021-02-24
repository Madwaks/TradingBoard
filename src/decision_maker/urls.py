from django.urls import path

from decision_maker.views.screener import ScreenerSelectionView

urlpatterns = [path("", ScreenerSelectionView.as_view())]
