# Generated by Django 2.2.20 on 2021-04-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200824_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=2, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='money',
            field=models.CharField(default=3, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=4, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='number',
            field=models.CharField(default=5, max_length=32),
            preserve_default=False,
        ),
    ]