import factory
from factory import SubFactory, RelatedFactoryList, enums

from core.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        strategy = enums.BUILD_STRATEGY

    name = factory.Faker("company")

    symbol = factory.Faker("pystr", max_chars=2)

    info = SubFactory("core.tests.factories.company_info.CompanyInfoFactory")

    quotes = RelatedFactoryList(
        "core.tests.factories.quotes.QuotesFactory",
        factory_related_name="company",
        size=201,
    )
