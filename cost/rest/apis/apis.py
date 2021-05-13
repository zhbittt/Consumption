from datetime import datetime

from django.db import transaction
from django.db.models import Sum, F
from rest_framework import permissions, mixins, exceptions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from cost.models import Bill, BillDetailRecord
from cost.rest.serializers import BillSerializers, BillDetailRecordSerializer


class BillApiSet(GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin):
    """
    账单
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = BillSerializers

    def get_queryset(self):
        return Bill.objects.filter(customer=self.request.user.customer).order_by('id')

    @action(methods=['get'], detail=False)
    def analysis(self, request, *args, **kwargs):
        res = {}
        customer = request.user.customer
        bills = Bill.objects.filter(
            customer=customer,
            pay_time__year=datetime.now().year,
            bill_detail_record__state=True).annotate(
            bill_amount=Sum(F('bill_detail_record__price') * F('bill_detail_record__number')))
        res['date'] = datetime.now().strftime('%Y')
        res['amount'] = bills.aggregate(total_amount=Sum('bill_amount'))['total_amount'] or 0
        res['values'] = []
        for month in bills.dates('pay_time', 'month'):
            month_bills = bills.filter(pay_time__month=month.month)
            month_values = {
                'date': month.strftime('%Y-%m'),
                'amount': month_bills.aggregate(month_amount=Sum('bill_amount'))['month_amount'] or 0,
                'values': []
            }
            for day in month_bills.dates('pay_time', 'day'):
                day_bills = month_bills.filter(pay_time__day=day.day)
                day_values = {
                    'date': day.strftime('%Y-%m-%d'),
                    'amount': day_bills.aggregate(day_amount=Sum('bill_amount'))['day_amount'] or 0,
                    'bill_details': []
                }
                for bill in day_bills:
                    day_values['bill_details'].extend(
                        BillDetailRecordSerializer(bill.bill_detail_record.filter(state=True), many=True).data)
                month_values['values'].append(day_values)
            res['values'].append(month_values)
        return Response(res)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(BillApiSet, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super(BillApiSet, self).update(request, *args, **kwargs)


class BillDetailRecordApiViewSet(GenericViewSet, mixins.UpdateModelMixin):
    """
    账单详细
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = BillDetailRecordSerializer

    def get_queryset(self):
        return BillDetailRecord.objects.filter(bill__customer=self.request.user.customer).order_by('id')
