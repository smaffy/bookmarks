from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

from taggit.forms import TagWidget

from .models import Image


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description', 'tags', )
        widgets = {
            'url': forms.HiddenInput,
            'tags': TagWidget(),
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        # download from url img
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image


class ImageAddForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'description', 'tags')
        widgets = {
            'tags': TagWidget(),
        }


class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'tags')
        widgets = {
            'tags': TagWidget(),
        }




