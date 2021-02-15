import factory
from factory import RelatedFactory

from core.models import Portfolio


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio
        strategy = factory.enums.BUILD_STRATEGY

    name = factory.Faker("company")
    amount = factory.Faker("random_int")

    positions = RelatedFactory(
        "core.tests.factories.position.PositionFactory",
        factory_related_name="portfolio",
    )
