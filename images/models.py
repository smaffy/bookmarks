from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager
from pytils import translit


class Image(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(AUTH_USER_MODEL, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit.slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

