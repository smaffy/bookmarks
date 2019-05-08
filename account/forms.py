from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Profile
from . import views


class LoginForm(forms.Form):
    username = forms.CharField(label='Username/Email:')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=mark_safe('I agree to the <a href="ppolice/">Privacy Policy</a> '
                                             'and <a href="terms/">Terms and Conditions</a>.'),
                             # label='I agree to the Privacy Policy and Terms of Use',
                             error_messages={'required': "You must agree to the terms to register"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():

            raise forms.ValidationError(mark_safe(
                ('Email addresses must be unique <a href="{0}">Help</a>').format(reverse(views.emailhelp))))
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birthdate', 'address', 'phone', 'photo')
        widgets = {
            'birthdate': forms.DateInput(format='%m/%d/%Y', attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class RemoveUser(forms.Form):
    username = forms.CharField()


class EmailUser(forms.Form):
    email = forms.EmailField()


class RestoreUser(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)