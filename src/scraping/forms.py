from django.forms import Form, ModelChoiceField, Select, CharField, TextInput, EmailField, EmailInput
from .models import City, ProgramLanguage


class FindForm(Form):
    city = ModelChoiceField(queryset=City.objects.all(),
                            to_field_name='slug',
                            required=False,
                            widget=Select(attrs={'class': 'form-control'}),
                            label='Місто')
    program_language = ModelChoiceField(queryset=ProgramLanguage.objects.all(),
                                        to_field_name='slug',
                                        required=False,
                                        widget=Select(attrs={'class': 'form-control'}),
                                        label='Мова програмування')


class ContactForm(Form):
    city = CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control'}),
        label='Місто'
    )
    program_language = CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control'}),
        label='Мова програмування'
    )
    email = EmailField(
        label='Введіть електронну пошту',
        widget=EmailInput(attrs={'class': 'form-control'})
    )
