# Generated by Django 2.2 on 2019-05-24 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_image_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
