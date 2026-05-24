from datetime import date

import pytest
from django.contrib.auth.models import User

from factory.models import (
    City, Client, Furniture, FurnitureModel, FurnitureType, Order, OrderItem, UserProfile,
)
from factory.views import _can_edit_order, _orders_for_user


@pytest.fixture
def client_user(db):
    user = User.objects.create_user(username='order_client', password='pass12345')
    UserProfile.objects.create(user=user, role=UserProfile.ROLE_CLIENT, phone='+375 (29) 111-11-11')
    city = City.objects.create(name='Минск')
    client = Client.objects.create(
        user=user,
        code='CL001',
        name='Тест',
        phone='+375 (29) 111-11-11',
        city=city,
        address='ул. Тест',
        birth_date=date(1990, 5, 1),
    )
    return user, client


@pytest.fixture
def furniture_item(db):
    ft = FurnitureType.objects.create(name='Кухни')
    fm = FurnitureModel.objects.create(name='Модель А')
    return Furniture.objects.create(
        code='ART-1', name='Стол', furniture_type=ft, model=fm, price=100,
    )


@pytest.mark.django_db
def test_client_sees_only_own_orders(client_user, furniture_item):
    user, client = client_user
    other_user = User.objects.create_user(username='other', password='pass12345')
    other_client = Client.objects.create(
        user=other_user, code='CL002', name='Другой',
        phone='+375 (29) 222-22-22', address='Адрес',
    )
    Order.objects.create(client=client, order_date=date.today(), status='new')
    Order.objects.create(client=other_client, order_date=date.today(), status='new')

    qs = _orders_for_user(user)
    assert qs.count() == 1


@pytest.mark.django_db
def test_client_can_edit_only_new_order(client_user, furniture_item):
    user, client = client_user
    order = Order.objects.create(client=client, order_date=date.today(), status='new')
    OrderItem.objects.create(order=order, furniture=furniture_item, quantity=1, price_per_unit=100)

    assert _can_edit_order(user, order) is True
    order.status = 'done'
    assert _can_edit_order(user, order) is False


@pytest.mark.django_db
def test_order_views_require_login(client):
    response = client.get('/orders/')
    assert response.status_code == 302
    assert '/login/' in response.url
