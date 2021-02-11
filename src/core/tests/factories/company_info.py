import factory

from core.models import CompanyInfo


class CompanyInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyInfo
        strategy = factory.enums.BUILD_STRATEGY

    yahoo_url = factory.Faker("uri")
    bourso_url = factory.Faker("uri")
    bfm_url = factory.Faker("uri")

    sector = None
    sub_sector = None
    creation_date = None
    quotes_file_path = None
