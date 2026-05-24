"""
Вспомогательные функции для описательной статистики (лаб. требования).

mean / median / mode считаются через стандартный модуль statistics Python.
Данные берутся из выполненных заказов (status='done') и профилей Client.
"""

from datetime import date
from statistics import mean, median, multimode

from django.db.models import Sum, F, DecimalField


def descriptive_stats(values):
    """
    Среднее, медиана, мода для списка чисел.
    Возвращает dict с округлением до 2 знаков.
    """
    nums = [float(v) for v in values if v is not None]
    if not nums:
        return {
            'count': 0,
            'mean': 0,
            'median': 0,
            'mode': None,
            'modes': [],
        }

    avg = mean(nums)
    med = median(nums)
    try:
        modes = multimode(nums)
    except Exception:
        modes = [nums[0]]

    return {
        'count': len(nums),
        'mean': round(avg, 2),
        'median': round(med, 2),
        'mode': round(modes[0], 2) if len(modes) == 1 else modes,
        'modes': [round(m, 2) for m in modes],
    }


def client_ages_years():
    """Возраст клиентов в годах (по birth_date)."""
    today = date.today()
    ages = []
    from .models import Client

    for client in Client.objects.exclude(birth_date__isnull=True):
        bd = client.birth_date
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        ages.append(age)
    return ages


def order_totals_done():
    """Суммы выполненных заказов (subtotal по позициям)."""
    from .models import Order

    totals = []
    for order in Order.objects.filter(status='done').prefetch_related('orderitem_set'):
        total = order.total_price()
        if total:
            totals.append(total)
    return totals


def item_subtotals_done():
    """Суммы по каждой позиции в выполненных заказах."""
    from .models import OrderItem

    return [
        float(item.subtotal())
        for item in OrderItem.objects.filter(order__status='done').select_related('order')
    ]


def profitable_furniture_types(limit=5):
    """Самые прибыльные виды мебели (по сумме продаж)."""
    from .models import OrderItem

    return (
        OrderItem.objects.filter(order__status='done')
        .values(name=F('furniture__furniture_type__name'))
        .annotate(
            revenue=Sum(
                F('quantity') * F('price_per_unit'),
                output_field=DecimalField(),
            ),
        )
        .order_by('-revenue')[:limit]
    )
