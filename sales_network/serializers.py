from rest_framework import serializers

from sales_network.models import NetworkNode, ContactInfo, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения продуктов сети.
    """
    class Meta:
        model = Product
        fields = '__all__'


class ContactInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения контактной информации сети.
    """
    class Meta:
        model = ContactInfo
        fields = '__all__'


class NetworkNodeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка сетей с подключенными продуктами и контактной информацией.
    """
    products = ProductSerializer(many=True, read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    level = serializers.IntegerField(source='get_level', read_only=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'


class NetworkNodeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления сети и контактной информации.
    """
    contact_info = ContactInfoSerializer()  # Для создания/обновления ContactInfo

    class Meta:
        model = NetworkNode
        exclude = ['created_at']
        # read_only_fields = ['debt']  # debt нельзя изменить через API

    def create(self, validated_data):
        """
        Создает новый объект NetworkNode вместе со связанным объектом ContactInfo.
        """
        contact_info_data = validated_data.pop('contact_info')  # Извлечение данных контактной информации
        contact_info = ContactInfo.objects.create(**contact_info_data)  # Создание объекта ContactInfo
        supplier = NetworkNode.objects.create(contact_info=contact_info, **validated_data)  # Создание поставщика

        return supplier

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект NetworkNode и его связанную контактную информацию.
        """
        contact_info_data = validated_data.pop('contact_info', None)  # Извлечение данных контактной информации

        if contact_info_data:
            for attr, value in contact_info_data.items():
                setattr(instance.contact_info, attr, value)  # Обновление полей ContactInfo
            instance.contact_info.save()  # Сохранение ContactInfo

        # Обновление полей поставщика
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
