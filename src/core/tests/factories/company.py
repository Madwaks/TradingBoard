from typing import Set

import factory
from factory import SubFactory, enums

from core.models import Company, Quote
from core.tests.factories.quotes import QuotesFactory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        strategy = enums.BUILD_STRATEGY
        django_get_or_create = ("name",)

    name = factory.Faker("company")

    symbol = factory.Faker("pystr", max_chars=2)

    info = SubFactory("core.tests.factories.company_info.CompanyInfoFactory")

    # quotes = RelatedFactoryList(
    #     "core.tests.factories.quotes.QuotesFactory",
    #     factory_related_name="company",
    #     size=201,
    # )
    quotes: Set[Quote] = None

    @factory.post_generation
    def quotes(self, create, extracted, **_kwargs):
        if extracted:
            while len(self.quotes.all()) <= 205:
                try:
                    self.quotes.add(
                        QuotesFactory.create(company=self)
                        if create
                        else QuotesFactory.build(company=self)
                    )
                except Exception:
                    continue
        else:
            self.quotes.add(
                QuotesFactory.create(company=self)
                if create
                else QuotesFactory.build(company=self)
            )
