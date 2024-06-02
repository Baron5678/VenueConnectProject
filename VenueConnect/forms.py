from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import User
import VenueConnect.validators as validators


class SignInForm(AuthenticationForm):
# usuario = forms.CharField(label='Username', max_length=100)
# contrasena = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        fields = ["usuario","contrasena"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])  # Custom defined email field

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Example: adding a regex validator to the username
        self.fields['first_name'].validators.append(
            validators.username_validator
        )
       
        self.fields['last_name'].validators.append(
            validators.username_validator
        )

        self.fields['phone_number'].validators.append(
            validators.phone_validator
        )

        self.fields['password1'].validators.append(
            validators.password_validator
        )

        self.fields['password2'].validators.append(
            validators.password_validator
        )


class NameAuthForm(AuthenticationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(NameAuthForm, self).__init__(*args, **kwargs)
        # Remove username field if you are not using it
        del self.fields['username']

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')

        if first_name and last_name and password:
            self.user_cache = authenticate(self.request, first_name=first_name, last_name=last_name, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid login details.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
