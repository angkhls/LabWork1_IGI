"""
Представления (Function-Based Views) мебельной фабрики.

Каждая функция:
  - GET: готовит QuerySet и отдаёт render(template, context).
  - POST: принимает форму, вызывает form.is_valid(), save(), redirect.

Права доступа — модуль access.py и декораторы login_required / role_required / client_only.
Логи — logger 'factory.views' (см. LOGGING в settings.py).
"""
import base64
import io
import logging

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Furniture, Review
from .forms import ReviewForm

from .access import (
    can_manage_catalog, can_manage_orders, can_use_cart, can_view_all_orders,
    get_user_role, is_registered_client,
)
from .decorators import client_only, role_required
from .forms import (
    ArticleForm, CustomRegistrationForm, FAQPublishForm, FAQQuestionForm, FurnitureForm,
    LoginForm, OrderAddItemForm, OrderEditForm, ReviewForm,
)
from .promo_utils import find_active_promo
from .stats_utils import (
    client_ages_years, descriptive_stats, item_subtotals_done,
    order_totals_done, profitable_furniture_types,
)
from .models import (
    Article, Client, CompanyInfo, Employee, FAQQuestion, Furniture, FurnitureType,
    Order, OrderItem, Promo, Review, UserProfile, Vacancy,
)

logger = logging.getLogger('factory.views')


def _orders_for_user(user):
    """QuerySet заказов: клиент видит только свои, персонал — все."""
    if can_view_all_orders(user):
        return Order.objects.select_related('client')
    if hasattr(user, 'client'):
        return Order.objects.filter(client=user.client).select_related('client')
    return Order.objects.none()


def _can_edit_order(user, order):
    """Редактирование: клиент — только свои «Новые»; персонал — «Новый» и «В работе»."""
    if order.status in ('done', 'cancelled'):
        return False
    if can_view_all_orders(user):
        return True
    if hasattr(user, 'client') and order.client == user.client:
        return order.status == 'new'
    return False


def _can_delete_order(user, order):
    if order.status == 'done':
        return False
    if can_view_all_orders(user):
        return True
    if hasattr(user, 'client') and order.client == user.client:
        return order.status in ('new', 'cancelled')
    return False


def home(request):
    """Главная: последняя опубликованная новость (публичная страница)."""
    article = Article.objects.filter(is_published=True).first()
    return render(request, 'factory/home.html', {'article': article})


def about(request):
    info = CompanyInfo.objects.all().order_by('year')
    return render(request, 'factory/about.html', {'info': info})


def privacy(request):
    return render(request, 'factory/privacy.html')


def news_list(request):
    articles = Article.objects.filter(is_published=True)
    q = request.GET.get('q', '')
    if q:
        articles = articles.filter(Q(title__icontains=q) | Q(summary__icontains=q))
    sort = request.GET.get('sort', '-published_at')
    if sort in ('published_at', '-published_at', 'title', '-title'):
        articles = articles.order_by(sort)
    return render(request, 'factory/news.html', {'articles': articles, 'q': q, 'sort': sort})


def news_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_published=True)
    return render(request, 'factory/news_detail.html', {'article': article})


@login_required
@role_required(UserProfile.ROLE_MANAGER, UserProfile.ROLE_DIRECTOR)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость добавлена.')
            return redirect('/news/')
    else:
        form = ArticleForm()
    return render(request, 'factory/article_form.html', {'form': form, 'title': 'Добавить новость'})


@login_required
@role_required(UserProfile.ROLE_MANAGER, UserProfile.ROLE_DIRECTOR)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость обновлена.')
            return redirect('/news/')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'factory/article_form.html', {'form': form, 'title': 'Редактировать новость'})


@login_required
@role_required(UserProfile.ROLE_MANAGER, UserProfile.ROLE_DIRECTOR)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Новость удалена.')
        return redirect('/news/')
    return render(request, 'factory/article_confirm_delete.html', {'article': article})


def furniture_list(request):
    items = Furniture.objects.select_related('furniture_type', 'model')
    q = request.GET.get('q', '')
    if q:
        items = items.filter(Q(name__icontains=q) | Q(code__icontains=q))
    ftype = request.GET.get('type', '')
    if ftype:
        items = items.filter(furniture_type_id=ftype)
    active = request.GET.get('active', '')
    if active:
        items = items.filter(is_active=(active == '1'))
    sort = request.GET.get('sort', 'name')
    if sort in ('name', '-name', 'price', '-price'):
        items = items.order_by(sort)
    types = FurnitureType.objects.all()
    return render(request, 'factory/furniture_list.html', {
        'items': items, 'types': types, 'q': q, 'ftype': ftype, 'sort': sort,
        'can_manage': can_manage_catalog(request.user),
    })



    

@login_required
def furniture_create(request):
    if not can_manage_catalog(request.user):
        messages.error(request, 'Недостаточно прав.')
        return redirect('/furniture/')
    if request.method == 'POST':
        form = FurnitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изделие добавлено.')
            return redirect('/furniture/')
    else:
        form = FurnitureForm()
    return render(request, 'factory/furniture_form.html', {'form': form, 'title': 'Добавить изделие'})

def furniture_detail(request, pk):
    furniture = get_object_or_404(Furniture, id=pk)
    reviews = Review.objects.filter(furniture=furniture).order_by('-created_at')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.furniture = furniture
            review.save()
            return redirect('furniture_detail', pk=furniture.id)
    else:
        form = ReviewForm()
        
    return render(request, 'factory/furniture_detail.html', {
        'item': furniture,
        'reviews': reviews,
        'form': form,
    })

@login_required
def furniture_edit(request, pk):
    if not can_manage_catalog(request.user):
        messages.error(request, 'Недостаточно прав.')
        return redirect('/furniture/')
    item = get_object_or_404(Furniture, pk=pk)
    if request.method == 'POST':
        form = FurnitureForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изделие обновлено.')
            return redirect('/furniture/')
    else:
        form = FurnitureForm(instance=item)
    return render(request, 'factory/furniture_form.html', {'form': form, 'title': 'Редактировать изделие'})


@login_required
def furniture_delete(request, pk):
    if not can_manage_catalog(request.user):
        messages.error(request, 'Недостаточно прав.')
        return redirect('/furniture/')
    item = get_object_or_404(Furniture, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Изделие удалено.')
        return redirect('/furniture/')
    return render(request, 'factory/furniture_confirm_delete.html', {'item': item})


def cart_add(request, furniture_id):
    furniture = get_object_or_404(Furniture, id=furniture_id)
    cart = request.session.get('cart', {})
    key = str(furniture_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'«{furniture.name}» добавлен в корзину.')
    return redirect('/cart/')


def cart_detail(request):
    from .models import PickupPoint

    session_cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for prod_id, quantity in session_cart.items():
        try:
            product = Furniture.objects.get(id=int(prod_id))
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total,
            })
        except Furniture.DoesNotExist:
            continue
    pickup_points = PickupPoint.objects.filter(is_active=True)
    return render(request, 'factory/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'pickup_points': pickup_points,
    })


def cart_remove(request, furniture_id):
    cart = request.session.get('cart', {})
    key = str(furniture_id)
    if key in cart:
        del cart[key]
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, 'Товар удалён из корзины.')
    return redirect('/cart/')

@login_required
def order_create(request):
    if not can_use_cart(request.user):
        messages.error(request, 'Оформление заказов доступно только зарегистрированным клиентам.')
        return redirect('/')

    if request.method == 'POST':
        session_cart = request.session.get('cart', {})
        if not session_cart:
            messages.error(request, 'Корзина пуста.')
            return redirect('/cart/')

        pickup_point = request.POST.get('pickup_point', '')
        delivery_address = request.POST.get('delivery_address', '')
        if not pickup_point or not delivery_address:
            messages.error(request, 'Заполните адрес и пункт самовывоза.')
            return redirect('/cart/')

        try:
            current_client = request.user.client
        except Client.DoesNotExist:
            messages.error(request, 'Профиль клиента не найден.')
            return redirect('/')

        promo_code = request.POST.get('promo_code', '').strip()
        promo_obj, promo_error = find_active_promo(promo_code)
        if promo_error:
            messages.warning(request, f'{promo_error} Заказ оформлен без скидки.')
        elif promo_obj:
            messages.success(
                request,
                f'Применён промокод «{promo_obj.code}»: скидка {promo_obj.discount_percent}%.',
            )

        order = Order.objects.create(
            client=current_client,
            order_date=timezone.now().date(),
            status='new',
            notes=f'Пункт: {pickup_point}. Адрес: {delivery_address}',
            promo=promo_obj,
        )

        for prod_id, quantity in session_cart.items():
            try:
                furniture = Furniture.objects.get(id=int(prod_id))
                OrderItem.objects.create(
                    order=order,
                    furniture=furniture,
                    quantity=quantity,
                    price_per_unit=furniture.price,
                )
            except Furniture.DoesNotExist:
                pass

        request.session['cart'] = {}
        request.session.modified = True

        total = order.total_price()
        if promo_obj:
            messages.success(
                request,
                f'Заказ #{order.pk} оформлен. '
                f'Сумма без скидки: {order.subtotal_before_discount()} BYN, '
                f'скидка: {order.discount_amount()} BYN, '
                f'к оплате: {total} BYN.',
            )
        else:
            messages.success(request, f'Заказ #{order.pk} оформлен. К оплате: {total} BYN.')
        return redirect('/orders/success/')

    return redirect('/cart/')

def faq_page(request):
    """Старый URL /faq/ — перенаправление на единую страницу словаря (FAQ)."""
    return redirect('/glossary/')


@login_required
def order_list(request):
    if not can_manage_orders(request.user):
        messages.error(
            request,
            'Раздел заказов доступен зарегистрированным клиентам и сотрудникам фабрики. '
            'Войдите как клиент (после регистрации) или как manager/director.',
        )
        return redirect('/login/' if not request.user.is_authenticated else '/')
    orders = _orders_for_user(request.user).select_related('client', 'promo').prefetch_related(
        'orderitem_set',
    )
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    sort = request.GET.get('sort', '-order_date')
    if sort in ('order_date', '-order_date', 'status'):
        orders = orders.order_by(sort)
    order_rows = [
        {
            'order': o,
            'can_edit': _can_edit_order(request.user, o),
            'can_delete': _can_delete_order(request.user, o),
        }
        for o in orders
    ]
    return render(request, 'factory/order_list.html', {
        'order_rows': order_rows,
        'status': status,
        'sort': sort,
        'can_create': can_use_cart(request.user),
    })


@login_required
def order_detail(request, pk):
    if not can_manage_orders(request.user):
        messages.error(request, 'Нет доступа к заказам.')
        return redirect('/')
    order = get_object_or_404(
        _orders_for_user(request.user).select_related('promo', 'client').prefetch_related(
            'orderitem_set__furniture',
        ),
        pk=pk,
    )
    items = order.orderitem_set.select_related('furniture').all()
    return render(request, 'factory/order_detail.html', {
        'order': order,
        'items': items,
        'subtotal': order.subtotal_before_discount(),
        'discount': order.discount_amount(),
        'total': order.total_price(),
        'can_edit': _can_edit_order(request.user, order),
        'can_delete': _can_delete_order(request.user, order),
    })


@login_required
def order_edit(request, pk):
    if not can_manage_orders(request.user):
        return redirect('/')
    order = get_object_or_404(
        _orders_for_user(request.user).prefetch_related('orderitem_set__furniture'),
        pk=pk,
    )
    if not _can_edit_order(request.user, order):
        messages.error(request, 'Этот заказ нельзя редактировать.')
        return redirect(f'/orders/{pk}/')

    items = order.orderitem_set.select_related('furniture').all()

    if request.method == 'POST':
        action = request.POST.get('action', 'save')

        if action == 'add_item':
            add_form = OrderAddItemForm(request.POST)
            if add_form.is_valid():
                furniture = add_form.cleaned_data['furniture']
                quantity = add_form.cleaned_data['quantity']
                existing = order.orderitem_set.filter(furniture=furniture).first()
                if existing:
                    existing.quantity += quantity
                    existing.save()
                else:
                    OrderItem.objects.create(
                        order=order,
                        furniture=furniture,
                        quantity=quantity,
                        price_per_unit=furniture.price,
                    )
                messages.success(request, 'Товар добавлен в заказ.')
            else:
                messages.error(request, 'Ошибка добавления товара.')
            return redirect(f'/orders/{pk}/edit/')

        if action == 'remove_item':
            item_id = request.POST.get('item_id')
            order.orderitem_set.filter(pk=item_id).delete()
            messages.success(request, 'Позиция удалена.')
            return redirect(f'/orders/{pk}/edit/')

        if action == 'save':
            edit_form = OrderEditForm(request.POST, instance=order, user=request.user)
            if edit_form.is_valid():
                edit_form.save()
                for item in items:
                    qty_key = f'quantity_{item.pk}'
                    if qty_key in request.POST:
                        try:
                            qty = int(request.POST[qty_key])
                            if qty < 1:
                                continue
                            item.quantity = qty
                            item.save()
                        except ValueError:
                            pass
                messages.success(request, 'Заказ обновлён.')
                return redirect(f'/orders/{pk}/')
            messages.error(request, 'Проверьте данные формы.')
        return redirect(f'/orders/{pk}/edit/')

    edit_form = OrderEditForm(instance=order, user=request.user)
    add_form = OrderAddItemForm()
    return render(request, 'factory/order_edit.html', {
        'order': order,
        'items': items,
        'edit_form': edit_form,
        'add_form': add_form,
    })


@login_required
def order_delete(request, pk):
    if not can_manage_orders(request.user):
        return redirect('/')
    order = get_object_or_404(_orders_for_user(request.user), pk=pk)
    if not _can_delete_order(request.user, order):
        messages.error(request, 'Этот заказ нельзя удалить.')
        return redirect(f'/orders/{pk}/')

    if request.method == 'POST':
        order.delete()
        messages.success(request, f'Заказ #{pk} удалён.')
        return redirect('/orders/')

    return render(request, 'factory/order_confirm_delete.html', {'order': order})


def order_success(request):
    return render(request, 'factory/order_success.html')


@login_required
@role_required(UserProfile.ROLE_DIRECTOR)
def client_list(request):
    clients = Client.objects.select_related('city').all()
    q = request.GET.get('q', '')
    if q:
        clients = clients.filter(Q(name__icontains=q) | Q(code__icontains=q))
    sort = request.GET.get('sort', 'name')
    if sort in ('name', '-name', 'code'):
        clients = clients.order_by(sort)
    return render(request, 'factory/client_list.html', {'clients': clients, 'q': q, 'sort': sort})


def glossary(request):
    """
    Словарь терминов и понятий (по ТЗ) = FAQ: вопрос, ответ, дата добавления.

    Публично показываются только записи с is_answered=True.
    Любой посетитель может отправить вопрос; ответ публикует менеджер/админ.
    """
    entries = FAQQuestion.objects.filter(is_answered=True).select_related('user')
    q = request.GET.get('q', '')
    if q:
        entries = entries.filter(
            Q(question_text__icontains=q) | Q(answer_text__icontains=q),
        )
    sort = request.GET.get('sort', '-created_at')
    if sort in ('created_at', '-created_at', 'question_text'):
        entries = entries.order_by(sort)

    ask_form = FAQQuestionForm()
    if request.method == 'POST' and request.POST.get('form_type') == 'ask':
        ask_form = FAQQuestionForm(request.POST)
        if ask_form.is_valid():
            entry = ask_form.save(commit=False)
            if request.user.is_authenticated:
                entry.user = request.user
            entry.is_answered = False
            entry.save()
            logger.info('Новый вопрос в словарь от %s', request.user)
            messages.success(request, 'Вопрос принят. Ответ появится после проверки.')
            return redirect('/glossary/')

    return render(request, 'factory/glossary.html', {
        'entries': entries,
        'q': q,
        'sort': sort,
        'ask_form': ask_form,
        'can_publish': can_manage_catalog(request.user),
    })


@login_required
@role_required(UserProfile.ROLE_MANAGER, UserProfile.ROLE_DIRECTOR)
def glossary_create(request):
    """Персонал публикует готовую пару вопрос–ответ в словаре (сразу на сайте)."""
    if request.method == 'POST':
        form = FAQPublishForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            logger.info('Опубликован FAQ: %s', request.user.username)
            messages.success(request, 'Запись добавлена в словарь.')
            return redirect('/glossary/')
    else:
        form = FAQPublishForm()
    return render(request, 'factory/glossary_form.html', {
        'form': form,
        'title': 'Добавить вопрос и ответ в словарь',
    })


def vacancies(request):
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'factory/vacancies.html', {'vacancies': vacancies_list})


@login_required
@client_only
def wholesale(request):
    """Оптовые закупки — только зарегистрированный клиент."""
    return render(request, 'factory/wholesale.html')


def reviews(request):
    """Отзывы: все видят список; форма добавления — только авторизованным."""
    all_reviews = Review.objects.select_related('user', 'furniture').all()
    form = ReviewForm() if request.user.is_authenticated else None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите или зарегистрируйтесь, чтобы оставить отзыв.')
            return redirect('/login/')
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен.')
            return redirect('/reviews/')
    return render(request, 'factory/reviews.html', {'reviews': all_reviews, 'form': form})


def promos(request):
    active = Promo.objects.filter(is_active=True)
    archive = Promo.objects.filter(is_active=False)
    return render(request, 'factory/promos.html', {'active': active, 'archive': archive})


def contacts(request):
    employees = Employee.objects.all()
    return render(request, 'factory/contacts.html', {'employees': employees})


def _build_sales_chart():
    """График продаж по видам мебели (matplotlib → base64 PNG)."""
    data = (
        OrderItem.objects.filter(order__status='done')
        .values('furniture__furniture_type__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
    )
    labels = [row['furniture__furniture_type__name'] or 'Без типа' for row in data]
    values = [row['total_qty'] or 0 for row in data]

    if not labels:
        labels = ['Нет данных']
        values = [0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color='#2c3e50')
    ax.set_title('Продажи по видам мебели (выполненные заказы)')
    ax.set_ylabel('Количество единиц')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


@login_required
@role_required(UserProfile.ROLE_DIRECTOR)
def statistics(request):
    furniture = Furniture.objects.order_by('name')
    popular_types = FurnitureType.objects.annotate(
        count=Count('furniture__orderitem'),
    ).order_by('-count')
    orders = Order.objects.filter(status='done')
    total = OrderItem.objects.filter(order__status='done').aggregate(
        total=Sum(F('quantity') * F('price_per_unit')),
    )['total'] or 0
    chart_base64 = _build_sales_chart()

    order_stats = descriptive_stats(order_totals_done())
    sales_line_stats = descriptive_stats(item_subtotals_done())
    age_stats = descriptive_stats(client_ages_years())
    profitable_types = profitable_furniture_types()

    return render(request, 'factory/statistics.html', {
        'furniture': furniture,
        'popular_types': popular_types,
        'orders': orders,
        'total': total,
        'chart_base64': chart_base64,
        'order_stats': order_stats,
        'sales_line_stats': sales_line_stats,
        'age_stats': age_stats,
        'profitable_types': profitable_types,
    })


def pickup_points(request):
    from .models import PickupPoint

    points = PickupPoint.objects.filter(is_active=True)
    return render(request, 'factory/pickup_points.html', {'points': points})
def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        
        # ВОТ ЭТА СТРОЧКА ОБЯЗАТЕЛЬНА! Без неё cleaned_data не появится
        if form.is_valid():
            # Создаем пользователя Django
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            # Создаем профиль
            UserProfile.objects.create(
                user=user,
                role=UserProfile.ROLE_CLIENT,
                birth_date=form.cleaned_data['birth_date']
            )
            
            # Создаем клиента
            Client.objects.create(
                user=user,
                code=f"CL-{user.pk}",
                name=form.cleaned_data['username'],
                birth_date=form.cleaned_data['birth_date']
            )
            
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('/')
    else:
        form = CustomRegistrationForm()

    return render(request, 'factory/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            messages.success(request, f'Добро пожаловать, {request.user.username}!')
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'factory/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
    return redirect('/')

def get_calendar_data():
    now = datetime.now()
    cal = calendar.HTMLCalendar(calendar.MONDAY)
    
    return cal.formatmonth(now.year, now.month)
