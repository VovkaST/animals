from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from animals.settings import DB_PREFIX
from shelter.validators import gt_current_date_validator


class NotDeletedManager(models.Manager):
    """ Менеджер, возвращающий только те записи, у которых нет отметки об удалении """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Shelter(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название приюта')
    address = models.CharField(null=True, blank=True, max_length=250, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')

    def __str__(self):
        return self.title

    class Meta:
        db_table = f'{DB_PREFIX}_shelters'
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'


class ShelterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='User')
    shelter = models.OneToOneField(Shelter, on_delete=models.CASCADE, verbose_name='Приют', related_name='Shelter')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    def __str__(self):
        return f'{self.user} ({self.shelter})'

    class Meta:
        db_table = f'{DB_PREFIX}_user'
        ordering = ['user']
        verbose_name = 'Дополнительная информация о пользователе'
        verbose_name_plural = 'Дополнительная информация о пользователе'


class Animals(models.Model):
    """ Животные, помещенные в приют """

    name = models.CharField(max_length=100, verbose_name='Кличка')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения',
                                  validators=(gt_current_date_validator,))
    arrive_date = models.DateField(default=timezone.now, verbose_name='Дата прибытия в приют',
                                   validators=(gt_current_date_validator,))
    weight = models.FloatField(default=0, verbose_name='Вес', validators=(MinValueValidator(0.1), ))
    height = models.FloatField(default=0, verbose_name='Рост', validators=(MinValueValidator(0.1), ))
    special_signs = models.CharField(max_length=1000, blank=True, verbose_name='Особые приметы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')
    is_deleted = models.BooleanField(default=False, verbose_name='Отметка об удалении')
    deleted_at = models.DateTimeField(null=True, verbose_name='Дата и время удаления')

    objects = models.Manager()
    actual_objects = NotDeletedManager()

    def __str__(self):
        return self.name

    @property
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
        verbose_name = 'Постоялец приюта'
        verbose_name_plural = 'Постояльцы приюта'
