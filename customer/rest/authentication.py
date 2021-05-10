from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from Consumption import settings


class BillTokenAuthentication(TokenAuthentication):

    def get_model(self):
        from customer.models import BillToken
        return BillToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        from customer.models import BillToken
        if token.type != BillToken.Types.ADMIN and (
                now() - token.created).total_seconds() > settings.TOKEN_EXPIRED_IN:
            raise exceptions.AuthenticationFailed(_('登录态已失效，请重新登录'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)

