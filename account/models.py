from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


def upload_path_handler(instance, filename):
    return "profileimg/{name}/{file}".format(name=instance.user.username, file=filename)


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
    address = models.CharField(max_length=150, null=True)
    phone = PhoneNumberField(null=True)
    photo = models.ImageField(upload_to=upload_path_handler, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        a = Profile.objects.create(user=instance)
#        a.save()


# post_save.connect(create_user_profile, sender=User)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()


