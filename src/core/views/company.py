from core.models import Company
from utils.mixins.view.filter_list import FilterListView


class CompanyList(FilterListView):
    template_name = "company_list.html"
    model = Company
