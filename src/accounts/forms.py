from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.forms import Form, EmailInput, CharField, PasswordInput, ValidationError

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