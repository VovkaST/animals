# Generated by Django 2.2 on 2020-09-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelter', '0011_auto_20200906_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelter',
            name='address',
            field=models.CharField(max_length=250, null=True, verbose_name='Адрес'),
        ),
    ]
