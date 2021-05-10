from rest_framework import serializers
from customer.models import Customer


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=3, required=True)

    class Meta:
        model = Customer
        fields = ('id', 'username', 'password')

