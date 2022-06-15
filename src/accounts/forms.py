from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.forms import (Form, ModelForm, EmailInput, CheckboxInput,
                          CharField, BooleanField, PasswordInput, ValidationError,
                          ModelChoiceField, Select, TextInput, EmailField)

from scraping.models import City, ProgramLanguage

User = get_user_model()


class UserLoginForm(Form):
    email = CharField(widget=EmailInput(attrs={'class': 'form-control'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise ValidationError('Такого користувача не має')
            if not check_password(password, qs[0].password):
                raise ValidationError('Не вірний пароль')

            user = authenticate(email=email, password=password)

            if not user:
                raise ValidationError('Користувач відключений')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(ModelForm):
    email = EmailField(label='Введіть електронну пошту', widget=EmailInput(attrs={'class': 'form-control'}))
    password1 = CharField(label='Введіть пароль', widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(label='Повторіть пароль', widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise ValidationError('Паролі не співпадають')
        return data['password2']


class UserUpdateForm(Form):
    city = ModelChoiceField(queryset=City.objects.all(),
                            to_field_name='slug',
                            required=True,
                            widget=Select(attrs={'class': 'form-control'}),
                            label='Місто'
                            )
    program_language = ModelChoiceField(queryset=ProgramLanguage.objects.all(),
                                        to_field_name='slug',
                                        required=True,
                                        widget=Select(attrs={'class': 'form-control'}),
                                        label='Мова програмування'
                                        )
    send_email = BooleanField(required=False,
                              widget=CheckboxInput,
                              label='Отримувати розсилку на пошту?'
                              )

    class Meta:
        model = User
        fields = ('city', 'program_language', 'send_email')


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