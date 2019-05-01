from django.db import models
from django.conf import settings


def upload_path_handler(instance, filename):
    return "profileimg/{name}/{file}".format(name=instance.user.username, file=filename)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=15, null=True)
    photo = models.ImageField(upload_to=upload_path_handler, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def create_userprofile(self, user, created):
        if created:
            Profile.objects.create(user=user)


