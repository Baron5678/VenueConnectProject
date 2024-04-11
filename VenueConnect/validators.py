from django.core.validators import RegexValidator

password_validator = RegexValidator(
    regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&(*)]{8,}$',
    message='Please, stick to requirements below',
    code='invalid_password'
)

username_validator = RegexValidator(
    regex=r'^[A-Za-z\d@_.+-]{1,150}$',
    message='Please, stick to requirements below',
    code='invalid_username'
)
