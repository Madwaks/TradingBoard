from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _

from decision_maker.models import Indicator
from decision_maker.models.enums import Operator, Condition


class IndicatorStateForm(forms.Form):
    indicator_1 = forms.ChoiceField(
        required=False, choices=Indicator.AvailableIndicators.choices, initial="MM7"
    )
    indicator_2 = forms.ChoiceField(
        required=False, choices=Indicator.AvailableIndicators.choices, initial="MM20"
    )

    operator = forms.ChoiceField(choices=Operator.choices)

    condition = forms.ChoiceField(choices=Condition.choices, initial="DISABLED")

    def clean(self):
        cleaned_data = super().clean()
        indicator_1 = cleaned_data.get("indicator_1")
        indicator_2 = cleaned_data.get("indicator_2")

        if indicator_1 == indicator_2:
            self.add_error(
                field="indicator_2",
                error=ValidationError(
                    _("Indicators should be different"), code="invalid"
                ),
            )

    def clean_operator(self):
        operator = self.cleaned_data.get("operator")
        if operator not in Operator.values:
            self.add_error(
                field="operator",
                error=ValidationError(
                    _(f"{operator} operator is not valid."), code="invalid"
                ),
            )

        return operator


class IndicatorStateBaseFormSet(BaseFormSet):
    pass


IndicatorStateFormSet = formset_factory(
    IndicatorStateForm,
    formset=IndicatorStateBaseFormSet,
    extra=5,
    max_num=20,
    min_num=1,
)
