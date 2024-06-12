from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator

from VenueConnect import validators
from .models import User, BookingOrder
from .models import User, VenueType


class SearchForm(forms.Form):
    venue_type = forms.ChoiceField(choices=VenueType.choices)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    min_capacity = forms.IntegerField(required=False)
    max_capacity = forms.IntegerField(required=False)
    available_from = forms.DateField(required=False)
    available_to = forms.DateField(required=False)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])  # Custom defined email field
    username = forms.CharField(max_length=150)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "email",
                  "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del self.fields['usable_password']

        # Example: adding a regex validator to the username
        self.fields['first_name'].validators.append(
            validators.username_validator
        )

        self.fields['last_name'].validators.append(
            validators.username_validator
        )

        self.fields['username'].validators.append(
            validators.username_validator
        )

        self.fields['phone_number'].validators.append(
            validators.phone_validator
        )


class NameAuthForm(AuthenticationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    field_order = ['first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingOrder
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
