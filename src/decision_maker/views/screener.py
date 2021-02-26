from logging import getLogger
from time import time

from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from core.models import Company
from decision_maker.forms.screener import IndicatorStateFormSet
from decision_maker.models.enums import Condition

logger = getLogger("django")


class ScreenerSelectionView(FormView):
    form_class = IndicatorStateFormSet
    template_name = "screener_selection.html"

    def form_valid(self, form: Form) -> HttpResponse:
        final_companies: QuerySet = Company.objects.all()
        start_time = time()
        for clean_data in form.cleaned_data:
            indicator1 = clean_data.get("indicator_1")
            operator = clean_data.get("operator")
            indicator2 = clean_data.get("indicator_2")
            condition = clean_data.get("condition")
            solved_query = Company.objects.resolve_indicator_query(
                indicator1=indicator1, operator=operator, indicator2=indicator2
            )
            if condition == Condition.AND:
                final_companies = final_companies.intersection(solved_query)
            elif condition == Condition.OR:
                final_companies = final_companies.union(solved_query)
        logger.info(time() - start_time)
        return HttpResponseRedirect(
            reverse(
                "core:companies",
                kwargs={"pks": [company.pk for company in final_companies]},
            )
        )
