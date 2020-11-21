from django.db import models


class Portfolio(models.Model):
    amount = models.FloatField()
    name = models.CharField(default="New Portfolio", max_length=128)

    def __str__(self):
        return self.name