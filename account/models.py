from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

import os


def upload_path_handler(instance, filename):
    return os.path.join("images/profileimg/{name}/{file}".format(name=instance.user.username, file=filename))


class Profile(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('n', 'None'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)

    is_confirmed = models.BooleanField(default=False)

    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='n', null=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    photo = models.ImageField(upload_to=upload_path_handler, default='images/profileimg/default/default.jpg')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


# add dynamically to User
User.add_to_class('following',
                  models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

