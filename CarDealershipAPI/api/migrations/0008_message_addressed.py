# Generated by Django 4.2.5 on 2023-09-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='addressed',
            field=models.BooleanField(default=0),
        ),
    ]