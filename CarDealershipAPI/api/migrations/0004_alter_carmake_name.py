# Generated by Django 4.2.5 on 2023-09-06 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_enginetype_car_featured_car_enginetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmake',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
