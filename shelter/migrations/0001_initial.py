# Generated by Django 2.2 on 2020-07-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Кличка')),
                ('birth_date', models.DateField(null=True, verbose_name='Дата рождения')),
                ('arrive_date', models.DateField(auto_now_add=True, verbose_name='Дата прибытия в приют')),
                ('weight', models.FloatField(default=0, verbose_name='Вес')),
                ('height', models.FloatField(default=0, verbose_name='Рост')),
                ('special_signs', models.CharField(max_length=1000, verbose_name='Особые приметы')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')),
            ],
            options={
                'verbose_name': 'Постояльцы приюта',
                'db_table': 'acits_animals',
                'ordering': ['-created_at'],
            },
        ),
    ]
