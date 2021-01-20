from django.db import models


class CompanyInfoUrl(models.Model):
    yahoo_url = models.CharField(
        max_length=256, default="http://finance.yahoo.com", null=True
    )
    bourso_url = models.CharField(max_length=256, blank=True, null=True)
    bfm_url = models.CharField(max_length=256, blank=True, null=True)
