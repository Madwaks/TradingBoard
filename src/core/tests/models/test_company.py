import pytest
from pytest_factoryboy import register

from core.models import Company, CompanyInfo
from core.tests.factories.company import CompanyFactory
from core.tests.factories.company_info import CompanyInfoFactory

register(CompanyInfoFactory)
register(CompanyFactory)


@pytest.mark.django_db
def test_company_model(company: Company):
    assert company.info
    assert str(company) == company.name
    assert not company.quotes.all()

    assert company.last_dated_quotation is None
    assert not company.is_up_to_date
    company.save()
    assert len(CompanyInfo.objects.all()) == 1
    assert len(Company.objects.all()) == 1


# @pytest.mark.django_db
# def test_company_info(empty_company_info: CompanyInfo):
#     assert empty_company_info.yahoo_url == "http://finance.yahoo.com"
#     assert len(CompanyInfo.objects.all()) == 1
#
#
# @pytest.mark.django_db
# def test_company_with_info(company: Company, company_info: CompanyInfo):
#     company.info = company_info
#     company.save()
#     assert not company.info.creation_date
#     assert company.info.quotes_file_path
#
#     assert len(CompanyInfo.objects.all()) == 1
#     assert len(Company.objects.all()) == 1
#
#
# @pytest.mark.django_db
# def test_company_with_quotes(quote: Quote, company: Company):
#     breakpoint()
