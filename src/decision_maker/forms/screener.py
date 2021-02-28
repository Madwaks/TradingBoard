from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms

from decision_maker.models import Screener
from utils.layouts.formset_layout import Formset


class ScreenerForm(forms.ModelForm):
    class Meta:
        model = Screener
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ScreenerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Div(
                Field("name"),
                Fieldset("Add conditions", Formset("conditions")),
                HTML("<br>"),
                ButtonHolder(Submit("submit", "save")),
            )
        )
