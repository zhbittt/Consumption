from rest_framework.exceptions import ValidationError


class NamedConst:
    choices = tuple()

    @classmethod
    def name_of(cls, v):
        for choice in cls.choices:
            if choice[0] == v:
                return choice[1]
        return "未知"


def validate_amount(value):
    if value is None:
        raise ValidationError('金额不能为空')
    if value and value < 0:
        raise ValidationError('金额不能为负')
