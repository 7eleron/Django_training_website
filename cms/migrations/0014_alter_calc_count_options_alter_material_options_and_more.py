# Generated by Django 4.0.5 on 2022-06-29 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cub_box_0', '0013_material_len'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calc_count',
            options={'verbose_name': 'Калькуляция', 'verbose_name_plural': 'Калькуляции'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Материал', 'verbose_name_plural': 'Материалы'},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'verbose_name': 'Работа', 'verbose_name_plural': 'Работы'},
        ),
    ]
