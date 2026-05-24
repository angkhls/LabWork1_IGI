from datetime import date
from decimal import Decimal

import pytest

from factory.models import City, Client, Furniture, FurnitureModel, FurnitureType, Order, OrderItem, Promo, UserProfile
from factory.promo_utils import find_active_promo
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_find_active_promo():
    Promo.objects.create(code='SAVE10', discount_percent=10, is_active=True)
    promo, err = find_active_promo('save10')
    assert promo is not None
    assert err is None

    promo2, err2 = find_active_promo('BAD')
    assert promo2 is None
    assert err2 is not None


@pytest.mark.django_db
def test_order_total_with_promo():
    user = User.objects.create_user(username='promo_cl', password='x')
    UserProfile.objects.create(user=user, role=UserProfile.ROLE_CLIENT, phone='+375 (29) 111-11-11')
    city = City.objects.create(name='М')
    client = Client.objects.create(
        user=user, code='P1', name='Co', phone='+375 (29) 111-11-11', city=city, address='a',
    )
    ft = FurnitureType.objects.create(name='T')
    fm = FurnitureModel.objects.create(name='M')
    furn = Furniture.objects.create(code='X', name='Стол', furniture_type=ft, model=fm, price=Decimal('100.00'))
    promo = Promo.objects.create(code='HALF', discount_percent=10, is_active=True)
    order = Order.objects.create(client=client, order_date=date.today(), promo=promo)
    OrderItem.objects.create(order=order, furniture=furn, quantity=2, price_per_unit=Decimal('100.00'))

    assert order.subtotal_before_discount() == Decimal('200.00')
    assert order.discount_amount() == Decimal('20.00')
    assert order.total_price() == Decimal('180.00')
