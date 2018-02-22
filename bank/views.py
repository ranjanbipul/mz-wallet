from rest_framework import permissions,viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class ImmutableViewSet(viewsets.GenericViewSet):
    """
        Allow object to be created but not updated or deleted
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AccountViewSet(ImmutableViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user_id=self.request.user.id)


class TransactionViewSet(ImmutableViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.id)
