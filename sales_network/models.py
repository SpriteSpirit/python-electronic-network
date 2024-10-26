from django.db import models

NULLABLE = {'null': True, 'blank': True}


class ContactInfo(models.Model):
    """
    Контактная информация
    """
    email = models.EmailField(max_length=255, verbose_name='Email')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=255, verbose_name='Номер дома')

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return f"{self.city}, {self.street} {self.house_number}"


class Supplier(models.Model):
    """
    Поставщик
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, verbose_name='Контактная информация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Товар
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class NetworkNode(models.Model):
    """
    Сеть (Завод, Розничная сеть, Индивидуальный предприниматель)
    """
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель')
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Уровень')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик', **NULLABLE)
    products = models.ManyToManyField(Product, verbose_name='Продукты', blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность перед поставщиком',
                               default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'
        ordering = ['-name']

    def __str__(self):
        return self.name
