import calendar
import logging
import urllib3
import requests
import zoneinfo
from datetime import datetime
from .access import build_nav_visibility, get_user_role
from .models import UserProfile

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger('factory.context')

def factory_global_context(request):
    role = get_user_role(request.user)
    nav = build_nav_visibility(request.user)

    # Значения по умолчанию
    context = {
        'usd_rate': '3,2500',
        'USER_CITY': 'Минск',
        'user_timezone': 'Europe/Minsk',
        'current_time_local': 'Ошибка времени',
        'current_time_utc': 'Ошибка времени',
        'text_calendar': '',
        'user_role': role,
        'user_role_label': '',
        'nav': nav,
        'is_guest': not request.user.is_authenticated,
    }

    # Роль пользователя
    if role == UserProfile.ROLE_CLIENT:
        context['user_role_label'] = 'Клиент'
    elif role == UserProfile.ROLE_MANAGER:
        context['user_role_label'] = 'Менеджер'
    elif role == UserProfile.ROLE_DIRECTOR:
        context['user_role_label'] = 'Директор'

    # API Курс валют
    try:
        response = requests.get('https://api.nbrb.by/exrates/rates/USD?parammode=2', timeout=2, verify=False)
        if response.status_code == 200:
            data = response.json()
            rate = data.get('Cur_OfficialRate')
            scale = data.get('Cur_Scale', 1)
            context['usd_rate'] = f'{round(rate / scale, 4)}'.replace('.', ',')
    except Exception as e:
        logger.debug('API NBRB недоступен: %s', e)

    # Время и Календарь
    try:
        # UTC время
        utc_now = datetime.now(zoneinfo.ZoneInfo('UTC'))
        context['current_time_utc'] = utc_now.strftime('%d/%m/%Y %H:%M:%S')
        
        # Местное время
        local_tz = zoneinfo.ZoneInfo(context['user_timezone'])
        local_now = datetime.now(local_tz)
        context['current_time_local'] = local_now.strftime('%d/%m/%Y %H:%M:%S')
    except Exception as e:
        logger.error('Ошибка времени: %s', e)

    # Текстовый календарь
    cal = calendar.TextCalendar(firstweekday=0)
    now = datetime.now()
    context['text_calendar'] = cal.formatmonth(now.year, now.month)

    return context