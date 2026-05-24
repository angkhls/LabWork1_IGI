from django.contrib import admin

from .models import (
    Article, City, Client, CompanyInfo, Employee, FAQQuestion, Furniture,
    FurnitureModel, FurnitureType, GlossaryTerm, Order, OrderItem, PickupPoint,
    Promo, Review, UserProfile, Vacancy,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['furniture', 'quantity', 'price_per_unit']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'birth_date']
    list_filter = ['role']


@admin.register(FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    """Словарь терминов на сайте = опубликованные FAQ (is_answered + answer_text)."""

    list_display = ['question_text', 'user', 'is_answered', 'created_at']
    list_filter = ['is_answered', 'created_at']
    search_fields = ['question_text', 'answer_text']

    def save_model(self, request, obj, form, change):
        if obj.answer_text and obj.answer_text.strip():
            obj.is_answered = True
        else:
            obj.is_answered = False
        super().save_model(request, obj, form, change)


@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'phone', 'email']
    list_filter = ['city']
    search_fields = ['name', 'code', 'phone']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'phone']
    search_fields = ['full_name', 'position']


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'furniture_type', 'model', 'price', 'is_active']
    list_filter = ['furniture_type', 'model', 'is_active']
    search_fields = ['code', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'employee', 'order_date', 'status']
    list_filter = ['status', 'order_date']
    search_fields = ['client__name']
    inlines = [OrderItemInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title']


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    """Архивная таблица; для лабы используйте FAQQuestion."""

    list_display = ['term', 'added_at']
    search_fields = ['term']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'furniture', 'rating', 'created_at']
    list_filter = ['rating']


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at_local', 'created_at_utc']
    list_filter = ['is_active', 'created_at_local']


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'valid_until']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'year']


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active']
