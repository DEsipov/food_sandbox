from django.contrib import admin

from core.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс настройки раздела игредиентов"""

    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
