import factory
from factory import SubFactory

from core.models import Quote
from core.tests.factories.company import CompanyFactory


class QuotesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote
        strategy = factory.enums.BUILD_STRATEGY

    date = factory.Faker("date")
    open = factory.Faker("random_int", min=5, max=15)
    high = factory.Faker("random_int", min=10, max=15)
    close = factory.Faker("random_int", min=5, max=15)
    low = factory.Faker("random_int", min=5, max=15)
    volume = factory.Faker("random_int", min=100, max=5000)

    company = SubFactory(CompanyFactory)
