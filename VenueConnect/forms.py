from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User
import VenueConnect.validators as validators

class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])  # Custom defined email field

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

      #   Example: adding a regex validator to the username
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
