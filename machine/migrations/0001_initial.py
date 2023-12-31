# Generated by Django 4.2.1 on 2023-11-22 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название станка')),
                ('external_fabric_id', models.IntegerField(null=True, verbose_name='Идентификатор машины как фабрики')),
                ('serial_port', models.CharField(max_length=50, verbose_name='Последовательный порт')),
            ],
            options={
                'verbose_name': 'Станок',
                'verbose_name_plural': 'Станки',
            },
        ),
    ]
