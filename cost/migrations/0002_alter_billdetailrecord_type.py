# Generated by Django 3.2 on 2021-05-13 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cost', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdetailrecord',
            name='type',
            field=models.SmallIntegerField(choices=[(1, '餐饮美食'), (2, '服饰装扮'), (3, '日用百货'), (4, '家居家装'), (5, '数码电器'), (6, '运动户外'), (7, '美容美发'), (8, '交通出行'), (9, '住房物业'), (10, '酒店旅游'), (11, '娱乐消费'), (12, '医疗健康'), (13, '保险'), (14, '充值缴费'), (16, '学习教育'), (15, '其他')], null=True, verbose_name='类型'),
        ),
    ]
