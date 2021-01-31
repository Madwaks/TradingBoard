import pytest

from data.models import Company
from data.utils.store_data.companies import CompanyStorer


@pytest.mark.django_db
def test_store_from_file(company_storer: CompanyStorer):
    assert len(Company.objects.all()) == 0
    company_storer.store_companies()
    companies_created = Company.objects.all()
    assert len(companies_created) == 3

    assert Company.objects.get(name="1000MERCIS")
    assert Company.objects.get(name="2CRSI")

    air_liquide = Company.objects.get(name="AIR LIQUIDE")
    assert air_liquide.symbol == "AI"
