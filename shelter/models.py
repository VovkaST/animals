from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from animals.settings.base import DB_PREFIX


class Animals(models.Model):
    """ Животные, помещенные в приют """

    name = models.CharField(max_length=100, verbose_name='Кличка')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')
    arrive_date = models.DateField(default=timezone.now, verbose_name='Дата прибытия в приют')
    weight = models.FloatField(default=0, verbose_name='Вес', validators=(MinValueValidator(0.1), ))
    height = models.FloatField(default=0, verbose_name='Рост', validators=(MinValueValidator(0.1), ))
    special_signs = models.CharField(max_length=1000, blank=True, verbose_name='Особые приметы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')
    is_deleted = models.BooleanField(default=False, verbose_name='Отметка об удалении')
    deleted_at = models.DateTimeField(null=True, verbose_name='Дата и время удаления')

    def __str__(self):
        return self.name

    def age(self):
        delta = relativedelta(datetime.now(), self.birth_date)
        if delta.years:
            return f'{delta.years} лет'
        elif delta.months:
            return f'{delta.months} месяцев'
        else:
            return f'{delta.days} дней'

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        db_table = f'{DB_PREFIX}_animals'
        ordering = ['-created_at']
        verbose_name = 'Постояльцы приюта'
        verbose_name_plural = 'Постояльцы приюта'
