import factory

from core.models import Quote, Company
from core.tests.factories.company import CompanyFactory


class QuotesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote
        strategy = factory.enums.BUILD_STRATEGY

    date = factory.Faker("date")
    open = 15
    high = 18
    close = 16
    low = 12
    volume = 200

    @factory.post_generation
    def company(self, create, extracted, **_kwargs):
        if extracted:
            self.zone = extracted
        else:
            fake = factory.faker.faker.Faker()
            if fake.boolean() and Company.objects.exists():
                self.company = Company.objects.get(
                    id=Company.objects.values_list("id", flat=True)[
                        fake.random_int(min=0, max=Company.objects.count() - 1)
                    ]
                )
            else:
                self.company = (
                    CompanyFactory.create() if create else CompanyFactory.build()
                )
