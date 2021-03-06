# Generated by Django 2.2 on 2020-09-06 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shelter', '0016_delete_shelteruser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShelterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('shelter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shelter', to='shelter.Shelter', verbose_name='Приют')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Дополнительная информация о пользователе',
                'verbose_name_plural': 'Дополнительная информация о пользователе',
                'db_table': 'acits_user',
                'ordering': ['user'],
            },
        ),
    ]
