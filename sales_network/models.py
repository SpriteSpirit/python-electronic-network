from django.db import models

NULLABLE = {'null': True, 'blank': True}


class ContactInfo(models.Model):
    """
    Контактная информация
    """
    objects = models.Manager()

    email = models.EmailField(max_length=255, verbose_name='Email')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=255, verbose_name='Номер дома')

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} {self.house_number}"


class NetworkNode(models.Model):
    """
    Сеть поставщик (Завод, Розничная сеть, Индивидуальный предприниматель)
    """
    objects = models.Manager()

    name = models.CharField(max_length=255, verbose_name='Название')
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Поставщик', **NULLABLE)
    products = models.ManyToManyField('Product', verbose_name='Товары', blank=True)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, verbose_name='Контактная информация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    debt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность перед поставщиком',
                               default=0.00)

    class Meta:
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_level(self):
        """
        Возвращает уровень вложенности узла в сети. 0 - завод, 1 и далее - последующие уровни.
        """

        level = 0
        current = self
        while current.supplier:
            level += 1
            current = current.supplier
        return level

    get_level.short_description = 'Уровень'  # для отображения в админке


class Product(models.Model):
    """
    Товар
    """
    objects = models.Manager()

    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
