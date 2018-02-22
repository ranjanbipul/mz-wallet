from rest_framework import serializers
from .models import *


class ValidatedModelSerializer(serializers.ModelSerializer):
    """ This class add model validation to Model Serializer """

    def validate(self, attrs):
        self.Meta.model(**attrs).clean()
        return attrs

    def validate_user(self, value):
        """ Will insert current authenticated user """
        return self.context["request"].user


class AccountSerializer(ValidatedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, default=None, read_only=True)
    class Meta:
        model = Account
        fields = '__all__'

class TransactionSerializer(ValidatedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, default=None, read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'
