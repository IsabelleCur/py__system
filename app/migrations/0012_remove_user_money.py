# Generated by Django 2.2.20 on 2021-04-22 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_user_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='money',
        ),
    ]