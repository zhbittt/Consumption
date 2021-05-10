from rest_framework import serializers

from cost.models import Bill, BillDetailRecord


class BillDetailRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillDetailRecord
        fields = ('id', 'name', 'number', 'price', 'state', 'amount', 'type', 'get_type_display')
        read_onlt_fields = ('id', 'amount')

    def update(self, instance, validated_data):
        print(validated_data)
        return super(BillDetailRecordSerializer, self).update(instance, validated_data)


class BillSerializers(serializers.ModelSerializer):
    bill_detail_record = BillDetailRecordSerializer(many=True)

    class Meta:
        model = Bill
        fields = ('id', 'customer', 'name', 'amount', 'pay_time', 'pay_type', 'get_pay_type_display', 'bill_detail_record')
        read_onlt_fields = ('id', 'amount')

    def validate(self, attrs):
        attrs['customer'] = self.context['request'].user.customer
        return attrs

    def create(self, validated_data):
        bill_detail_record = validated_data.pop('bill_detail_record', [])
        instance = super(BillSerializers, self).create(validated_data)
        self.create_bill_detail_record(instance, bill_detail_record)
        return instance

    def update(self, instance, validated_data):
        bill_detail_record = validated_data.pop('bill_detail_record', [])
        instance.bill_detail_record.all().delete()
        instance = super(BillSerializers, self).update(instance, validated_data)
        self.create_bill_detail_record(instance, bill_detail_record)
        return instance

    def create_bill_detail_record(self, instance, bill_detail_records):
        for record in bill_detail_records:
            BillDetailRecord.objects.create(
                bill=instance,
                name=record['name'],
                number=record['number'],
                price=record['price'],
                type=record['type'],
                state=record.get('state') or True,
            )


