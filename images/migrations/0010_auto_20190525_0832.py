# Generated by Django 2.2 on 2019-05-25 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0009_auto_20190525_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
