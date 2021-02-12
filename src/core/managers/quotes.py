from django.db.models import Manager
from pandas import DataFrame


class QuoteManager(Manager):
    def get_as_dataframe(self):
        return DataFrame(list(self.all().values()))
