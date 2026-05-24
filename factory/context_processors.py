"""
Контекст-процессор: данные для ВСЕХ шаблонов (меню, API, время, права).

Вызывается Django автоматически перед рендером каждой страницы.
"""
import calendar
import logging
import urllib3
from datetime import datetime

import requests
import zoneinfo

from .access import build_nav_visibility, get_user_role
from .models import UserProfile

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger('factory.context')


def factory_global_context(request):
    """
    Добавляет в шаблон:
    - курс USD и геолокацию (внешние API);
    - локальное/UTC время и текстовый календарь;
    - роль пользователя и флаги видимости пунктов меню (nav).
    """
    role = get_user_role(request.user)
    nav = build_nav_visibility(request.user)

    context = {
        'usd_rate': '3,2500',
        'USER_CITY': 'Минск',
        'user_timezone': 'Europe/Minsk',
        'current_time_local': '',
        'current_time_utc': '',
        'text_calendar': '',
        'user_role': role,
        'user_role_label': '',
        'nav': nav,
        'is_guest': not request.user.is_authenticated,
    }

    if role == UserProfile.ROLE_CLIENT:
        context['user_role_label'] = 'Клиент (зарегистрирован)'
    elif role == UserProfile.ROLE_MANAGER:
        context['user_role_label'] = 'Менеджер'
    elif role == UserProfile.ROLE_DIRECTOR:
        context['user_role_label'] = 'Директор / владелец'
    elif request.user.is_authenticated:
        context['user_role_label'] = 'Пользователь без роли'

    try:
        response_nbrb = requests.get(
            'https://api.nbrb.by/exrates/rates/USD?parammode=2',
            timeout=2,
            verify=False,
        )
        if response_nbrb.status_code == 200:
            data_nbrb = response_nbrb.json()
            rate = data_nbrb.get('Cur_OfficialRate')
            scale = data_nbrb.get('Cur_Scale', 1)
            if rate is not None:
                final_rate = round(rate / scale, 4)
                context['usd_rate'] = f'{final_rate}'.replace('.', ',')
    except Exception as exc:
        logger.debug('API NBRB недоступен: %s', exc)

    try:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR', '')

        if ip_address in ('127.0.0.1', 'localhost', '::1'):
            ip_address = '37.214.42.22'

        response_ip = requests.get(
            f'http://ip-api.com/json/{ip_address}?fields=status,city,timezone',
            timeout=1.5,
        )
        if response_ip.status_code == 200:
            data_ip = response_ip.json()
            if data_ip.get('status') == 'success':
                if data_ip.get('city'):
                    context['USER_CITY'] = data_ip.get('city')
                if data_ip.get('timezone'):
                    context['user_timezone'] = data_ip.get('timezone')
    except Exception as exc:
        logger.debug('Геолокация недоступна: %s', exc)

    try:
        utc_now = datetime.now(zoneinfo.ZoneInfo('UTC'))
        context['current_time_utc'] = utc_now.strftime('%d/%m/%Y %H:%M:%S')
        local_tz = zoneinfo.ZoneInfo(context['user_timezone'])
        local_now = datetime.now(local_tz)
        context['current_time_local'] = local_now.strftime('%d/%m/%Y %H:%M:%S')
    except Exception as exc:
        logger.debug('Ошибка времени: %s', exc)

    cal = calendar.TextCalendar(firstweekday=0)
    now = datetime.now()
    context['text_calendar'] = cal.formatmonth(now.year, now.month)

    return context
