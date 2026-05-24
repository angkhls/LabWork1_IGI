import pytest

from factory.forms import CustomRegistrationForm


@pytest.mark.django_db
def test_registration_password_mismatch():
    form = CustomRegistrationForm(data={
        'username': 'testuser_unique_x',
        'company_name': 'ООО Тест',
        'client_code': 'CODE999X',
        'birth_date': '1990-01-01',
        'phone': '+375 (29) 123-45-67',
        'address': 'Минск',
        'password': 'secret1',
        'password_confirm': 'secret2',
    })
    assert not form.is_valid()
    assert 'Пароли не совпадают' in str(form.errors)
