from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

phone_validator = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message='Формат телефона: +375 (29) XXX-XX-XX',
)


def validate_adult(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Регистрация доступна только лицам старше 18 лет.')
    if age > 120:
        raise ValidationError('Укажите корректную дату рождения.')


class UserProfile(models.Model):
    """Профиль пользователя с ролью (RBAC). One-to-One с User."""

    ROLE_CLIENT = 'client'
    ROLE_MANAGER = 'manager'
    ROLE_DIRECTOR = 'director'
    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Клиент'),
        (ROLE_MANAGER, 'Менеджер'),
        (ROLE_DIRECTOR, 'Директор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default=ROLE_CLIENT)
    birth_date = models.DateField('Дата рождения', validators=[validate_adult], null=True, blank=True)
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[phone_validator],
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    def clean(self):
        if self.birth_date:
            validate_adult(self.birth_date)

    def is_client(self):
        return self.role == self.ROLE_CLIENT

    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    def is_director(self):
        return self.role == self.ROLE_DIRECTOR


class FAQQuestion(models.Model):
    """
    Словарь терминов / FAQ (одна сущность по ТЗ лабораторной).

    На сайте в разделе «Словарь» показываются записи с is_answered=True:
    вопрос, ответ и created_at (дата добавления).
    """

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор вопроса',
    )
    question_text = models.TextField('Вопрос')
    answer_text = models.TextField('Ответ', blank=True, null=True)
    is_answered = models.BooleanField('Опубликовано на сайте', default=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Вопрос-Ответ'
        verbose_name_plural = 'Вопросы и ответы'
        ordering = ['-created_at']

    def __str__(self):
        author = self.user.username if self.user else 'Гость'
        return f'Вопрос от {author}: {self.question_text[:30]}...'

    def clean(self):
        if self.answer_text and self.answer_text.strip():
            self.is_answered = True
        elif not self.answer_text:
            self.is_answered = False


class City(models.Model):
    name = models.CharField('Город', max_length=100)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Client(models.Model):
    """Клиент (оптовый заказчик). One-to-One с User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField('Код клиента', max_length=20, unique=True)
    name = models.CharField('Название компании', max_length=200)
    birth_date = models.DateField(
        'Дата рождения', validators=[validate_adult], null=True, blank=True,
    )
    phone = models.CharField('Телефон', max_length=20, validators=[phone_validator])
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Город')
    address = models.TextField('Адрес')
    email = models.EmailField('Email', blank=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.birth_date:
            validate_adult(self.birth_date)
        if self.email and '@' not in self.email:
            raise ValidationError({'email': 'Некорректный email.'})


class Employee(models.Model):
    """Сотрудник. One-to-One с User (опционально, для менеджеров)."""

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee',
    )
    full_name = models.CharField('ФИО', max_length=255)
    birth_date = models.DateField(
        'Дата рождения', validators=[validate_adult], null=True, blank=True,
    )
    email = models.EmailField('Электронная почта', blank=True, null=True)
    phone = models.CharField('Номер телефона', max_length=20, validators=[phone_validator])
    position = models.CharField('Должность', max_length=100)
    photo = models.ImageField('Фото', upload_to='employees/', blank=True, null=True)
    work_description = models.TextField('Описание работ', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.full_name} — {self.position}'

    def clean(self):
        if self.birth_date:
            validate_adult(self.birth_date)


class FurnitureType(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Вид изделия'
        verbose_name_plural = 'Виды изделий'

    def __str__(self):
        return self.name


class FurnitureModel(models.Model):
    name = models.CharField('Название модели', max_length=100)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return self.name


class Furniture(models.Model):
    code = models.CharField('Артикул', max_length=50, unique=True)
    name = models.CharField('Название', max_length=200)
    furniture_type = models.ForeignKey(FurnitureType, on_delete=models.CASCADE, verbose_name='Вид')
    model = models.ForeignKey(FurnitureModel, on_delete=models.CASCADE, verbose_name='Модель')
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
    )
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото', upload_to='furniture/', blank=True)
    is_active = models.BooleanField('В производстве', default=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['name']

    def __str__(self):
        return f'{self.code} — {self.name}'

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной.'})

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Клиент',
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Сотрудник',
    )
    items = models.ManyToManyField(Furniture, through='OrderItem', verbose_name='Изделия')
    order_date = models.DateField('Дата заказа')
    completion_date = models.DateField('Дата выполнения', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField('Примечания', blank=True)
    promo = models.ForeignKey(
        'Promo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Применённый промокод',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.client}'

    def clean(self):
        if self.completion_date and self.order_date and self.completion_date < self.order_date:
            raise ValidationError('Дата выполнения не может быть раньше даты заказа.')

    def subtotal_before_discount(self):
        """Сумма позиций без скидки."""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.orderitem_set.all():
            total += item.subtotal()
        return total

    def discount_amount(self):
        """Сумма скидки по промокоду (0 если промокода нет)."""
        from decimal import Decimal
        if not self.promo_id:
            return Decimal('0')
        percent = Decimal(self.promo.discount_percent)
        return self.subtotal_before_discount() * percent / Decimal('100')

    def total_price(self):
        """Итог к оплате: сумма позиций минус скидка промокода."""
        return self.subtotal_before_discount() - self.discount_amount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, verbose_name='Изделие')
    quantity = models.PositiveIntegerField('Количество')
    price_per_unit = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def subtotal(self):
        return self.quantity * self.price_per_unit

    def clean(self):
        if self.quantity < 1:
            raise ValidationError({'quantity': 'Количество должно быть не меньше 1.'})


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    summary = models.CharField('Краткое содержание', max_length=500)
    content = models.TextField('Полный текст')
    image = models.ImageField('Картинка', upload_to='articles/', blank=True)
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class GlossaryTerm(models.Model):
    """
    Устаревшая модель (term/definition). На сайте не используется.

    Актуальный «Словарь» — модель FAQQuestion. Данные можно перенести вручную в админке.
    """

    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    added_at = models.DateField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Термин (архив)'
        verbose_name_plural = 'Термины (архив, не на сайте)'

    def __str__(self):
        return self.term


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE, verbose_name='Товар', related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField('Оценка', choices=[(i, i) for i in range(1, 6)])
    text = models.TextField('Текст отзыва')
    image = models.ImageField('Фото к отзыву', upload_to='reviews_photos/', null=True, blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user} — {self.rating}★'

    def clean(self):
        if self.rating and (self.rating < 1 or self.rating > 5):
            raise ValidationError({'rating': 'Оценка от 1 до 5.'})


class PickupPoint(models.Model):
    name = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=300)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пункт самовывоза'
        verbose_name_plural = 'Пункты самовывоза'

    def __str__(self):
        return f'{self.name} ({self.address})'


class Vacancy(models.Model):
    title = models.CharField('Должность', max_length=200)
    description = models.TextField('Описание')
    is_active = models.BooleanField('Активна', default=True)
    created_at_utc = models.DateTimeField('Добавлено (UTC)', auto_now_add=True)
    created_at_local = models.DateTimeField('Добавлено (локально)', null=True, blank=True)
    updated_at_utc = models.DateTimeField('Изменено (UTC)', auto_now=True)
    updated_at_local = models.DateTimeField('Изменено (локально)', null=True, blank=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        import zoneinfo

        local_tz = zoneinfo.ZoneInfo('Europe/Minsk')
        local_now = timezone.now().astimezone(local_tz)
        if not self.pk:
            self.created_at_local = local_now
        self.updated_at_local = local_now
        super().save(*args, **kwargs)


class Promo(models.Model):
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField('Скидка %')
    is_active = models.BooleanField('Активен', default=True)
    valid_until = models.DateField('Действует до', null=True, blank=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f'{self.code} — {self.discount_percent}%'

    def clean(self):
        if self.discount_percent > 100:
            raise ValidationError({'discount_percent': 'Скидка не может превышать 100%.'})
        if self.valid_until and self.valid_until < date.today():
            raise ValidationError({'valid_until': 'Дата окончания не может быть в прошлом.'})


class CompanyInfo(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст')
    year = models.PositiveIntegerField('Год', null=True, blank=True)

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

    def __str__(self):
        return self.title
