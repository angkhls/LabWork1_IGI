"""
Декораторы для Function-Based Views.

role_required оборачивает view и проверяет роль до выполнения тела функции.
При отказе — сообщение пользователю и редирект (без CBV).
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .access import get_user_role, log_access_denied
from .models import UserProfile


def role_required(*roles):
    """
    Декоратор: разрешить вызов view только перечисленным ролям.

    Пример:
        @login_required
        @role_required(UserProfile.ROLE_DIRECTOR)
        def statistics(request): ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Необходима авторизация.')
                return redirect('/login/')

            role = get_user_role(request.user)
            if role is None:
                log_access_denied(request.user, view_func.__name__, 'no profile')
                messages.error(request, 'Профиль пользователя не настроен.')
                return redirect('/')

            if role not in roles:
                log_access_denied(request.user, view_func.__name__, f'role={role}')
                messages.error(request, 'Недостаточно прав для этой страницы.')
                return redirect('/')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def client_only(view_func):
    """Только зарегистрированный клиент (оптовые закупки, корзина)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from .access import is_registered_client

        if not is_registered_client(request.user):
            log_access_denied(request.user, view_func.__name__, 'clients only')
            messages.error(request, 'Раздел доступен только зарегистрированным клиентам.')
            return redirect('/login/' if not request.user.is_authenticated else '/')
        return view_func(request, *args, **kwargs)

    return wrapper
