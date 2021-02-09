from django.db import models


class CompanyInfo(models.Model):
    yahoo_url = models.CharField(
        max_length=256, default="http://finance.yahoo.com", null=True
    )
    bourso_url = models.CharField(max_length=256, blank=True, null=True)
    bfm_url = models.CharField(max_length=256, blank=True, null=True)
    sector = models.CharField(max_length=256, blank=True, null=True)
    sub_sector = models.CharField(max_length=256, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)

    quotes_file_path = models.CharField(max_length=128, blank=True, null=True)
