from django.urls import path

from trading_board.views.home import TradingBoardHome
from trading_board.views.portfolio import PortfolioListView, PortfolioView
from trading_board.views.trade_list import TradeListView

urlpatterns = [
    path("", TradingBoardHome.as_view()),
    path("trades/", TradeListView.as_view()),
    path("portfolios/", PortfolioListView.as_view()),
    path(r"portfolio/<int:pk>/", PortfolioView.as_view(), name="portfolio"),
]
