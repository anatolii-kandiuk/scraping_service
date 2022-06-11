from django.forms import Form, ModelChoiceField, Select
from .models import City, ProgramLanguage


class FindForm(Form):
    city = ModelChoiceField(queryset=City.objects.all(),
                            to_field_name='slug',
                            required=False,
                            widget=Select(attrs={'class': 'form-control'}),
                            label='City')
    program_language = ModelChoiceField(queryset=ProgramLanguage.objects.all(),
                                        to_field_name='slug',
                                        required=False,
                                        widget=Select(attrs={'class': 'form-control'}),
                                        label='Program language')

