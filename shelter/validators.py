from datetime import datetime

from django.core.exceptions import ValidationError


def gt_current_date_validator(date: datetime.date):
    """
    Валидатор проверяет, что введенное значение даты меньше текущей.
    Если значение больше или равно текущей, выбрасывается ValidationError
    :param date: Дата для валидации
    """
    if date > datetime.now().date():
        raise ValidationError('Указанная дата больше текущей')
