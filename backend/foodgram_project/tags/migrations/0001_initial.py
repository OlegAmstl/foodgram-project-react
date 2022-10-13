# Generated by Django 2.2.20 on 2022-05-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название', max_length=200, unique=True, verbose_name='Название')),
                ('color', models.CharField(help_text='Цвет в HEX', max_length=7, unique=True, verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(help_text='Уникальный слаг', max_length=200, unique=True, verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('slug',),
            },
        ),
    ]