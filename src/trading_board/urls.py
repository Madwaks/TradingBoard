from django.urls import path

from trading_board.views.home import TradingBoardHome
from trading_board.views.portfolio import (
    PortfolioListView,
    AddPortfolio,
    EditPortfolio,
    DeletePortfolio,
)
from trading_board.views.trade_list import TradeListView


urlpatterns = [
    path("", TradingBoardHome.as_view()),
    path("trades/", TradeListView.as_view()),
    path("portfolios/", PortfolioListView.as_view(), name="portfolios"),
    path("add-portfolio/", AddPortfolio.as_view()),
    path(
        "delete-portfolio/<int:portfolio_id>",
        DeletePortfolio.as_view(),
        name="delete_portfolio",
    ),
    path(
        "edit-portfolio/<int:portfolio_id>",
        EditPortfolio.as_view(),
        name="edit_portfolio",
    ),
]
