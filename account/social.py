from django.contrib.auth.models import User
from requests import request, HTTPError
from django.core.files.base import ContentFile
from social_django.models import UserSocialAuth

from .models import Profile


def get_or_create_profile(strategy, details, response, user, *args, **kwargs):

    if Profile.objects.filter(user=user).exists():
        pass
    else:
        new_profile = Profile(user=user)
        new_profile.save()

    return kwargs


def save_profile_picture(user, response, *args, **kwargs):
    try:
        facebook_login = user.social_auth.get(provider='facebook')

    except:
        facebook_login = None

    if facebook_login:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user.profile
            profile.photo.save('{0}_social.jpg'.format(user.username), ContentFile(response.content))
            profile.save()


