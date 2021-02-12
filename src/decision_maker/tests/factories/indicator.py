import factory
from factory import SubFactory

from core.tests.factories.company import CompanyFactory
from decision_maker.models import Indicator


class IndicatorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Indicator
        strategy = factory.enums.BUILD_STRATEGY

    date = factory.Faker("date")
    open = factory.Faker("random_int", min=5, max=15)
    high = factory.Faker("random_int", min=10, max=15)
    close = factory.Faker("random_int", min=5, max=15)
    low = factory.Faker("random_int", min=5, max=15)
    volume = factory.Faker("random_int", min=100, max=5000)

    company = SubFactory(CompanyFactory)
