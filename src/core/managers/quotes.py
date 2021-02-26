from typing import TYPE_CHECKING

from django.db.models import Manager
from django.db.models.query import QuerySet
from pandas import DataFrame

if TYPE_CHECKING:
    from core.models import Company


class QuoteManager(Manager):
    def get_as_dataframe(self) -> DataFrame:
        return DataFrame(list(self.all().values()))

    def get_last_company_quote(self, company: "Company") -> "QuerySet":
        return self.filter(company=company).latest("date")
