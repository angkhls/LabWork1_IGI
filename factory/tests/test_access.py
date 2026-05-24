import pytest
from django.contrib.auth.models import AnonymousUser, User

from factory.access import build_nav_visibility
from factory.models import Client, UserProfile


def test_guest_nav_hides_orders():
    nav = build_nav_visibility(AnonymousUser())
    assert nav['show_orders'] is False
    assert nav['show_statistics'] is False


@pytest.mark.django_db
def test_client_nav_shows_cart_not_statistics():
    user = User.objects.create_user(username='nav_client', password='x')
    UserProfile.objects.create(user=user, role=UserProfile.ROLE_CLIENT, phone='+375 (29) 111-11-11')
    Client.objects.create(
        user=user, code='N1', name='Co', phone='+375 (29) 111-11-11', address='a',
    )
    nav = build_nav_visibility(user)
    assert nav['show_cart'] is True
    assert nav['show_statistics'] is False
