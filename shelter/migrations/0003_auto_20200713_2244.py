# Generated by Django 2.2 on 2020-07-13 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelter', '0002_auto_20200713_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animals',
            name='special_signs',
            field=models.CharField(default=None, max_length=1000, null=True, verbose_name='Особые приметы'),
        ),
    ]
