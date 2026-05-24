from datetime import date

import pytest
from django.core.exceptions import ValidationError

from factory.models import validate_adult, phone_validator


@pytest.mark.parametrize(
    'phone,ok',
    [
        ('+375 (29) 123-45-67', True),
        ('+375291234567', False),
        ('80291234567', False),
    ],
)
def test_phone_validator(phone, ok):
    if ok:
        phone_validator(phone)
    else:
        with pytest.raises(ValidationError):
            phone_validator(phone)


def test_validate_adult_rejects_minor():
    young = date.today().replace(year=date.today().year - 10)
    with pytest.raises(ValidationError):
        validate_adult(young)


def test_validate_adult_accepts_adult():
    adult = date.today().replace(year=date.today().year - 25)
    validate_adult(adult)
