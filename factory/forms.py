"""
Формы сайта: валидация на бэкенде (is_valid) дублирует/усиливает HTML5 на фронте.

Словарь терминов по ТЗ = FAQ (вопрос + ответ + дата), модель FAQQuestion.
"""


from .models import Review
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator 
from datetime import date

from .models import (
    Article, City, Client, FAQQuestion, Furniture, Order, Review,
    UserProfile, phone_validator, validate_adult,
)


phone_regex = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате: +375 (29) XXX-XX-XX'
)

class CustomRegistrationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя (Логин)", max_length=150)
    birth_date = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={'type': 'date'}))
    # Добавляем поле телефона
    phone = forms.CharField(
        label="Телефон",
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67'}),
        help_text="Формат: +375 (29) XXX-XX-XX"
    )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput())

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise ValidationError('Регистрация доступна только лицам старше 18 лет.')
        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'required': True}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        user = authenticate(
            self.request,
            username=cleaned.get('username'),
            password=cleaned.get('password'),
        )
        if user is None:
            raise forms.ValidationError('Неверный логин или пароль.')
        cleaned['user'] = user
        return cleaned


class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = [
            'code', 'name', 'furniture_type', 'model',
            'price', 'description', 'photo', 'is_active',
        ]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'image', 'is_published']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'image']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i}★') for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'placeholder': 'Напишите ваш отзыв...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required = False
        self.fields['image'].required = False


class FAQQuestionForm(forms.ModelForm):
    """
    Форма для гостя/клиента: задать вопрос (ответ появится после модерации в админке).
    """

    class Meta:
        model = FAQQuestion
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Введите ваш вопрос...',
                'required': True,
            }),
        }
        labels = {'question_text': 'Ваш вопрос'}


class FAQPublishForm(forms.ModelForm):
    """
    Форма для /директора: сразу опубликовать пару вопрос–ответ в словаре.
    """

    class Meta:
        model = FAQQuestion
        fields = ['question_text', 'answer_text']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2, 'required': True}),
            'answer_text': forms.Textarea(attrs={'rows': 4, 'required': True}),
        }
        labels = {
            'question_text': 'Вопрос',
            'answer_text': 'Ответ',
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.is_answered = bool(instance.answer_text and instance.answer_text.strip())
        if user and user.is_authenticated:
            instance.user = user
        if commit:
            instance.save()
        return instance


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['notes', 'status']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        role = None
        if user and user.is_authenticated:
            profile = getattr(user, 'profile', None)
            role = profile.role if profile else None
        if role == UserProfile.ROLE_CLIENT:
            self.fields.pop('status', None)


class OrderAddItemForm(forms.Form):
    furniture = forms.ModelChoiceField(
        label='Изделие',
        queryset=Furniture.objects.filter(is_active=True),
        widget=forms.Select(attrs={'required': True}),
    )
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'required': True, 'min': 1}),
    )
