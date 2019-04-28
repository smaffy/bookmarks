from django.db import models
from django.db import models
from django.conf import settings

path = lambda instance, filename: 'images/{username}/{filename}'.format(
    username=instance.user.username, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=path, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


