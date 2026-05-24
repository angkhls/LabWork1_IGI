"""
Проверка и применение промокодов при оформлении заказа.
"""

from datetime import date

from .models import Promo


def find_active_promo(code):
    """
    Ищет промокод по коду.

    Возвращает (promo, error_message):
      - (Promo, None) — код найден и действует;
      - (None, str) — ошибка для сообщения пользователю;
      - (None, None) — поле промокода пустое.
    """
    if not code or not str(code).strip():
        return None, None

    normalized = str(code).strip()
    try:
        promo = Promo.objects.get(code__iexact=normalized, is_active=True)
    except Promo.DoesNotExist:
        return None, 'Промокод не найден или неактивен.'

    if promo.valid_until and promo.valid_until < date.today():
        return None, f'Промокод «{promo.code}» истёк ({promo.valid_until.strftime("%d/%m/%Y")}).'

    return promo, None
