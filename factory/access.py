"""
Модуль разграничения доступа (RBAC) для мебельной фабрики.

Три уровня пользователей по методичке:
  1. Гость (User без регистрации) — только публичные страницы.
  2. Зарегистрированный клиент (User + UserProfile.role=client + Client) — заказы, корзина, отзывы.
  3. Владелец / персонал — superuser или UserProfile.role=director (директор),
     менеджер (manager) — расширенные права без статистики и базы клиентов.

Все проверки собраны здесь, чтобы views и шаблоны не дублировали логику.
"""

import logging

from .models import UserProfile

logger = logging.getLogger('factory.access')


def get_user_role(user):
    """
    Определяет строковый код роли текущего пользователя.

    - Не авторизован → None (гость).
    - is_superuser → director (владелец магазина = полный доступ).
    - Иначе берётся role из связанной модели UserProfile.
  """
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserProfile.ROLE_DIRECTOR
    profile = getattr(user, 'profile', None)
    if profile:
        return profile.role
    return None


def is_guest(user):
    """Гость: не вошёл в систему."""
    return not user.is_authenticated


def is_registered_client(user):
    """Зарегистрированный клиент с профилем Client (может оформлять заказы)."""
    return (
        user.is_authenticated
        and get_user_role(user) == UserProfile.ROLE_CLIENT
        and hasattr(user, 'client')
    )


def is_manager(user):
    return get_user_role(user) == UserProfile.ROLE_MANAGER


def is_director(user):
    """Директор или Django superuser (владелец)."""
    return get_user_role(user) == UserProfile.ROLE_DIRECTOR


def can_manage_catalog(user):
    """CRUD каталога и новостей: менеджер и директор."""
    return get_user_role(user) in (UserProfile.ROLE_MANAGER, UserProfile.ROLE_DIRECTOR)


def can_view_all_orders(user):
    """Видеть все заказы фабрики (не только свои)."""
    return can_manage_catalog(user)


def can_view_statistics(user):
    """Статистика и графики — только директор / superuser."""
    return is_director(user)


def can_view_client_database(user):
    """Список всех клиентов — только директор / superuser."""
    return is_director(user)


def can_publish_glossary(user):
    """Публиковать готовые пары вопрос–ответ в словаре (FAQ)."""
    return can_manage_catalog(user)


def can_use_cart(user):
    return is_registered_client(user)


def can_manage_orders(user):
    """Доступ к разделу заказов (свои или все)."""
    if not user.is_authenticated:
        return False
    return is_registered_client(user) or can_view_all_orders(user)


def build_nav_visibility(user):
    """
    Флаги для меню в base.html — каждый пункт показывается только нужной группе.

    Возвращает словарь show_* чтобы гости не видели заказы, статистику и т.д.
    """
    role = get_user_role(user)
    return {
        # Публичное меню — у всех
        'show_public_menu': True,
        # Заказы: только авторизованные клиенты и персонал
        'show_orders': can_manage_orders(user),
        'show_cart': can_use_cart(user),
        'show_wholesale': is_registered_client(user),
        # Управление контентом
        'show_catalog_manage': can_manage_catalog(user),
        'show_news_manage': can_manage_catalog(user),
        'show_glossary_manage': can_publish_glossary(user),
        # Только владелец
        'show_statistics': can_view_statistics(user),
        'show_clients': can_view_client_database(user),
        'show_admin_link': is_director(user),
        # Отзыв можно оставить только авторизованным
        'show_review_form_hint': user.is_authenticated,
    }


def log_access_denied(user, resource, reason=''):
    """Запись в лог при отказе в доступе (для отчёта по лабораторной)."""
    username = user.username if user.is_authenticated else 'guest'
    logger.warning('ACCESS_DENIED user=%s resource=%s %s', username, resource, reason)
