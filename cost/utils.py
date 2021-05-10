from rest_framework.exceptions import ValidationError

def validate_amount(value):
    if value is None:
        raise ValidationError('金额不能为空')
    if value and value < 0:
        raise ValidationError('金额不能为负')
