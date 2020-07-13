from django.db import models

from animals.settings.base import DB_PREFIX


class Animals(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кличка')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')
    arrive_date = models.DateField(auto_now_add=True, verbose_name='Дата прибытия в приют')
    weight = models.FloatField(default=0, verbose_name='Вес')
    height = models.FloatField(default=0, verbose_name='Рост')
    special_signs = models.CharField(max_length=1000, verbose_name='Особые приметы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')

    class Meta:
        db_table = f'{DB_PREFIX}_animals'
        ordering = ['-created_at']
        verbose_name = 'Постояльцы приюта'
