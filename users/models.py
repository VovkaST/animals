from django.conf import settings
from django.db import models

from animals.settings import DB_PREFIX
from shelter.models import Shelter


class ShelterUser(models.Model):
    """ Дополнительная информация о пользователе """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='user')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, verbose_name='Приют', related_name='shelter')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    def __str__(self):
        return f'{self.user} ({self.shelter})'

    class Meta:
        db_table = f'{DB_PREFIX}_user'
        ordering = ['user']
        verbose_name = 'Дополнительная информация о пользователе'
        verbose_name_plural = 'Дополнительная информация о пользователе'
