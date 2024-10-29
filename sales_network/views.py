from rest_framework import viewsets, status
from rest_framework.response import Response

from sales_network.models import NetworkNode
from sales_network.serializers import NetworkNodeListSerializer, NetworkNodeCreateUpdateSerializer
from .permissions import IsActiveUser


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Управление сетями.
    """
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора.
        Для запросов GET используется NetworkNodeListSerializer,
        для запросов POST, PUT и PATCH используется NetworkNodeCreateUpdateSerializer.
        """

        if self.action in ('list', 'retrieve'):
            return NetworkNodeListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return NetworkNodeCreateUpdateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        """
        Возвращает список сетей, отфильтрованных по стране
        """

        queryset = super().get_queryset()
        country = self.request.query_params.get('country')

        if country:
            queryset = queryset.filter(contact_info__country=country)

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Обновляет сеть с проверкой наличия задолженности.
        Если задолженность есть, возвращает ошибку.
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Запрет обновления поля debt
        if 'debt' in serializer.validated_data:
            return Response({'detail': 'Изменение задолженности через API запрещено.'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
