from django import forms
from django.contrib.auth.forms import UserCreationForm

from authorizations.constants import COUNTRY_NAME_LEN, PHONE_NUMBER_LEN
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail",
    )
    phone_number = forms.CharField(
        max_length=PHONE_NUMBER_LEN,
        required=False,
        label="Номер телефона",
    )
    country = forms.CharField(
        max_length=COUNTRY_NAME_LEN,
        required=False,
        label="Страна",
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone_number",
            "country",
            "password1",
            "password2",
        ]
