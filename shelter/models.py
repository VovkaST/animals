from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from animals.middleware.request_user import get_current_user
from animals.settings import DB_PREFIX
from shelter.validators import gt_current_date_validator


class NotDeletedManager(models.Manager):
    """ Менеджер, возвращающий только те записи, у которых нет отметки об удалении """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Shelter(models.Model):
    """ Модель приюта """
    title = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(null=True, blank=True, max_length=250, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')

    def __str__(self):
        return self.title

    class Meta:
        db_table = f'{DB_PREFIX}_shelters'
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'


class Animals(models.Model):
    """ Модель животного, помещенного в приют """

    name = models.CharField(max_length=100, verbose_name='Кличка')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения',
                                  validators=(gt_current_date_validator,))
    arrive_date = models.DateField(default=timezone.now, verbose_name='Дата прибытия в приют',
                                   validators=(gt_current_date_validator,))
    weight = models.FloatField(default=0, verbose_name='Вес', validators=(MinValueValidator(0.1), ))
    height = models.FloatField(default=0, verbose_name='Рост', validators=(MinValueValidator(0.1), ))
    special_signs = models.CharField(max_length=1000, blank=True, verbose_name='Особые приметы')
    shelter = models.ForeignKey(Shelter, null=True, on_delete=models.CASCADE, verbose_name='Приют')
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
        """ Мягкое удаление записи (проставление отметки is_deleted = True без физического удаления) """
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """ Сохранение записи и проставление связи с Приютом, связанным с пользователем """
        from users.models import ShelterUser
        if not self.shelter:
            self.shelter = ShelterUser.objects.get(user=get_current_user()).shelter
        super(Animals, self).save(force_insert=force_insert, force_update=force_update,
                                  using=using, update_fields=update_fields)

    class Meta:
        db_table = f'{DB_PREFIX}_animals'
        ordering = ['-created_at']
        verbose_name = 'Постоялец приюта'
        verbose_name_plural = 'Постояльцы приюта'
