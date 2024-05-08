from django.core.validators import RegexValidator

password_validator = RegexValidator(
    regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&(*)]{8,}$',
    message='Password must have al least 8 characters and contain a letter and a number.',
    code='invalid_password'
)

username_validator = RegexValidator(
    regex=r'^[A-Za-z\d@_.+-]{1,150}$',
    message='Please, stick to requirements below',
    code='invalid_username'
)

phone_validator = RegexValidator(
    regex=r'^\+?\d{1,3}?[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$|^\d+$',
    message='Please, stick to requirements below',
    code='invalid_phone_number'
)
