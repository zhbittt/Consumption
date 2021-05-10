import binascii
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from Consumption import settings
from Consumption.utils.utils import NamedConst


# Create your models here.


class User(AbstractUser):  # 管理后台用户和消费者用户用is_staff区分
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    @property
    def is_customer(self):
        return not self.is_staff


class Customer(models.Model):

    username = models.CharField('用户名', unique=True, max_length=20)
    password = models.CharField('密码', max_length=100)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class BillToken(models.Model):
    class Types(NamedConst):
        ADMIN = 0
        WECHAT = 1
        ANDROID = 2
        IOS = 3

        choices = (
            (ADMIN, '后台'),
            (WECHAT, '微信'),
            (ANDROID, '安卓'),
            (IOS, '苹果'),
        )

    type = models.SmallIntegerField('用户Token', choices=Types.choices, default=Types.WECHAT)
    key = models.CharField(_('key'), max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        unique_together = ['user', 'type']

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(BillToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
