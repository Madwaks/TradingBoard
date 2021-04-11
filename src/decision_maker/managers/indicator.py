from typing import TYPE_CHECKING

from django.db.models import Manager

if TYPE_CHECKING:
    from core.models import Company


class IndicatorManager(Manager):
    def get_last_indicators_for_company(self, company: "Company"):
        for ind in self.all():
            if ind.quote.company == company:
                pass

        return self.filter()
