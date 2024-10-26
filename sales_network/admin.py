from django.db.models import F

from django.contrib import admin
from .models import NetworkNode, Product, ContactInfo


class LevelListFilter(admin.SimpleListFilter):
    """
    Фильтр по уровню сети
    """
    title = 'Уровень'  # Заголовок фильтра
    parameter_name = 'level'

    def lookups(self, request, model_admin):
        # Возвращает список вариантов для фильтра
        return (
            (0, 'Завод'),
            (1, 'Розничная сеть'),
            (2, 'Индивидуальный предприниматель'),
        )

    def queryset(self, request, queryset):
        """
        Фильтрует queryset на основе выбранного значения
        """
        value = self.value()
        # Преобразуем значение в число и применим фильтр к queryset'у, если оно указано'
        if value is not None:
            try:
                level = int(value)
                return queryset.annotate(level=F('get_level')).filter(level=level)
            except ValueError:
                # Обработка некорректных значений
                return queryset
        return queryset


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Админка сетей
    """
    list_display = ('name', 'get_level', 'supplier', 'debt')
    list_filter = ('contact_info__country', 'created_at', 'supplier', LevelListFilter)
    readonly_fields = ('created_at',)
    actions = ['clear_debt']

    @admin.action(description='Очистить задолженность')
    def clear_debt(self, request, queryset):
        queryset.update(debt=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка товаров
    """
    list_display = ('name', 'model', 'release_date')  # Убрали supplier
    list_filter = ('release_date',)  # Убрали supplier


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Админка контактных данных
    """
    list_display = ('email', 'country', 'city', 'street', 'house_number')
