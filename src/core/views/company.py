from django.views.generic import ListView

from core.models import Company


class CompanyListView(ListView):
    model = Company
