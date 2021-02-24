from typing import TYPE_CHECKING

from django.db.models import Manager
from pandas import DataFrame

if TYPE_CHECKING:
    from core.models import Company


class QuoteManager(Manager):
    def get_as_dataframe(self):
        return DataFrame(list(self.all().values()))

    def get_last_company_quote(self, company: "Company"):
        return self.filter(company=company).latest("date")
