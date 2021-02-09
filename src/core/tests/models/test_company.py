import pytest

from core.models import Company, CompanyInfo


@pytest.mark.django_db
def test_company_model(company: Company):
    assert company.name == "Tradefox"
    assert company.symbol == "ALTR"

    assert not company.info

    assert str(company) == "Tradefox"

    assert not company.last_dated_quotation

    assert not company.is_up_to_date
    company.save()
    assert len(Company.objects.all() == 1)


def test_company_info_url(empty_company_info: CompanyInfo):
    pass
