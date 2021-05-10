# Generated by Django 3.2 on 2021-05-10 08:18

import Consumption.utils.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='账单名称')),
                ('pay_time', models.DateTimeField(null=True, verbose_name='消费时间')),
                ('pay_type', models.SmallIntegerField(choices=[(1, '现金'), (2, '微信'), (3, '支付宝'), (4, '信用卡')], verbose_name='支付方式')),
                ('customer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='customer.customer', verbose_name='用户')),
            ],
            options={
                'verbose_name': '消费账单',
                'verbose_name_plural': '消费账单',
            },
        ),
        migrations.CreateModel(
            name='BillDetailRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('number', models.IntegerField(default=0, verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[Consumption.utils.utils.validate_amount], verbose_name='价格')),
                ('state', models.BooleanField(default=True, verbose_name='状态')),
                ('type', models.SmallIntegerField(choices=[(1, '餐饮美食'), (2, '服饰装扮'), (3, '日用百货'), (4, '家居家装'), (5, '数码电器'), (6, '运动户外'), (7, '美容美发'), (8, '交通出行'), (9, '住房物业'), (10, '酒店旅游'), (11, '娱乐消费'), (12, '医疗健康'), (13, '保险'), (14, '充值缴费'), (15, '其他')], null=True, verbose_name='类型')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bill_detail_record', to='cost.bill')),
            ],
            options={
                'verbose_name': '消费账单明细',
                'verbose_name_plural': '消费账单明细',
            },
        ),
    ]