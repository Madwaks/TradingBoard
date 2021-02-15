import factory
from factory import SubFactory
from factory.fuzzy import FuzzyChoice

from core.models import Position


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position
        strategy = factory.enums.BUILD_STRATEGY

    date = factory.Faker("date")
    nb_titres = factory.Faker("random_int")
    price = factory.Faker("pyfloat", positive=True)
    take_profit = factory.Faker("pyfloat", positive=True)
    stop_loss = factory.Faker("pyfloat", positive=True)

    reason_closed = FuzzyChoice(Position.ReasonClosed, getter=lambda c: c)

    portfolio = SubFactory("core.tests.factories.portfolio.PortfolioFactory")
