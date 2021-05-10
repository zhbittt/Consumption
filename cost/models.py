from django.db import models
from django.db.models import Sum, F, Count
from Consumption.utils.utils import NamedConst, validate_amount
from customer.models import Customer


# Create your models here.

class Bill(models.Model):

    class PayType(NamedConst):
        CASH = 1
        WECHAT = 2
        ALIPAY = 3
        CARD = 4

        choices = (
            (CASH, '现金'),
            (WECHAT, '微信'),
            (ALIPAY, '支付宝'),
            (CARD, '信用卡'),
        )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='用户', blank=True)
    name = models.CharField('账单名称', max_length=20)
    pay_time = models.DateTimeField('消费时间', null=True)
    pay_type = models.SmallIntegerField('支付方式', choices=PayType.choices)

    class Meta:
        verbose_name = '消费账单'
        verbose_name_plural = verbose_name

    @property
    def amount(self):
        return self.bill_detail_record.filter(state=True).aggregate(amount=Sum(F('price') * F('number')))['amount'] or 0


class BillDetailRecord(models.Model):
    class Types(NamedConst):
        FOOD = 1
        CLOTHING = 2
        DAILY_USE = 3
        FURNISHINGS = 4
        ELECTRONICS = 5
        OUTDOOR_SPORTS = 6
        BEAUTY_SALON = 7
        TRAFFIC = 8
        HOUSING = 9
        TOURISM = 10
        ENTERTAINMENT = 11
        HEALTH = 12
        INSURANCE = 13
        RECHARGE = 14
        OTHER = 15

        choices = (
            (FOOD, '餐饮美食'),
            (CLOTHING, '服饰装扮'),
            (DAILY_USE, '日用百货'),
            (FURNISHINGS, '家居家装'),
            (ELECTRONICS, '数码电器'),
            (OUTDOOR_SPORTS, '运动户外'),
            (BEAUTY_SALON, '美容美发'),
            (TRAFFIC, '交通出行'),
            (HOUSING, '住房物业'),
            (TOURISM, '酒店旅游'),
            (ENTERTAINMENT, '娱乐消费'),
            (HEALTH, '医疗健康'),
            (INSURANCE, '保险'),
            (RECHARGE, '充值缴费'),
            (OTHER, '其他'),
        )

    name = models.CharField('名称', max_length=20)
    number = models.IntegerField('数量', default=0)
    price = models.DecimalField('价格', max_digits=15, decimal_places=2, default=0, validators=[validate_amount])
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, related_name='bill_detail_record')
    state = models.BooleanField('状态', default=True)
    type = models.SmallIntegerField('类型', choices=Types.choices, null=True)

    class Meta:
        verbose_name = '消费账单明细'
        verbose_name_plural = verbose_name

    @property
    def amount(self):
        return self.number * self.price


