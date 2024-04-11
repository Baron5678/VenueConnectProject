from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User
import VenueConnect.validators as validators


class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])  # Custom defined email field

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Example: adding a regex validator to the username
        self.fields['username'].validators.append(
            validators.username_validator
        )

        self.fields['password1'].validators.append(
            validators.password_validator
        )

        self.fields['password2'].validators.append(
            validators.password_validator
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
