# Generated by Django 2.2 on 2019-05-13 20:30

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='media/profileimg/default/default.png', upload_to=account.models.upload_path_handler),
        ),
    ]