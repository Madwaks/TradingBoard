import factory
from factory import SubFactory

from core.models import Company
from core.tests.factories.company_info import CompanyInfoFactory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        strategy = factory.enums.BUILD_STRATEGY

    name = factory.Faker("company")

    symbol = factory.Faker("pystr", max_chars=2)

    info = SubFactory(CompanyInfoFactory)
