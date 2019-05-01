# Generated by Django 2.2 on 2019-05-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20190501_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.PositiveIntegerField(null=True),
        ),
    ]