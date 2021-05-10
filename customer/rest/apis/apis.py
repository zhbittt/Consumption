import uuid
from datetime import datetime
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.response import Response

from customer.models import Customer, BillToken, User
from customer.rest.serializers import LoginSerializer


class Login(GenericAPIView):
    """
    用户登录注册接口
    """
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()
    serializer_class = LoginSerializer

    def register(self, username, password):
        customer = Customer.objects.create(
            username=username,
            password=password)
        User.objects.create(
            customer=customer, username=uuid.uuid4())
        return customer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            login = True
            customer = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            login = False
            customer = self.register(username, password)

        if login:
            # 一个用户只允许一端登录
            BillToken.objects.filter(user=customer.user).delete()
        token, created = BillToken.objects.get_or_create(user=customer.user)
        if not created:
            token.key = token.generate_key()
            token.created = datetime.now()
            token.user = customer.user
            token.save()
        return Response({
            'login': login,
            'token': token.key
        })


class Logout(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        BillToken.objects.filter(user=request.user).delete()
        return Response('登出成功')
