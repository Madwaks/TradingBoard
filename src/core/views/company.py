from django.views.generic import ListView

from core.models import Company


class CompanyList(ListView):
    template_name = "company_list.html"
    model = Company

    def get_context_data(self, *, object_list=None, **kwargs):
        breakpoint()
