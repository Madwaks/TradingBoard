from factory import SubFactory, DjangoModelFactory, enums, Faker, RelatedFactory

from core.models import Quote


class QuotesFactory(DjangoModelFactory):
    class Meta:
        model = Quote
        strategy = enums.BUILD_STRATEGY
        django_get_or_create = ("date", "company")

    date = Faker("date")
    open = Faker("random_int", min=10, max=15)
    high = Faker("random_int", min=10, max=15)
    close = Faker("random_int", min=5, max=15)
    low = Faker("random_int", min=5, max=10)
    volume = Faker("random_int", min=100, max=5000)

    company = SubFactory("core.tests.factories.company.CompanyFactory")

    indicators = RelatedFactory(
        "decision_maker.tests.factories.indicator.IndicatorFactory",
        factory_related_name="quote",
    )
