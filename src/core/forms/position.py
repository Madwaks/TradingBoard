from django.forms import ModelForm

from core.models.position import Position


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
