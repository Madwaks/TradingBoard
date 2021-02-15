import pytest

from core.models import Company, CompanyInfo


@pytest.mark.django_db
def test_company_model(company: Company):
    assert company.info
    assert str(company) == company.name

    assert company.last_dated_quotation
    assert not company.is_up_to_date
    company.save()
    assert len(CompanyInfo.objects.all()) == 1
    assert len(Company.objects.all()) == 1
