from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, RemoveUser, EmailUser
from .models import Profile
from .tokens import account_activation_token



# without classes
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data

                user = authenticate(request, username=cd['username'], password=cd['password'])
                conf = Profile.objects.get(user=user)
                if user is not None:
                    if not conf.is_confirmed:
                        messages.error(request, 'Your account is not confirmed by email.')
                        return redirect('reActivation')
                    else:
                        if user.is_active:
                            login(request, user)
                            messages.success(request, 'Authenticated successfully')
                            return redirect('dashboard')
                        else:
                            login(request, user)
                            messages.error(request, 'Your account is inactive!')
                            return redirect('setactive')
                else:
                    messages.error(request, 'Invalid login or password')
                    return redirect('login')
        else:
            form = LoginForm()
            return render(request, 'registration/login.html', {'form': form})




def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    password_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    if not facebook_login:
        if not twitter_login:
            if not google_login:
                password_login = request.user.username

    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'facebook_login': facebook_login,
                                                      'twitter_login': twitter_login,
                                                      'google_login': google_login,
                                                      'password_login': password_login
                                                      })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.is_active = False
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)

            # confirm by email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/activate.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('reActivation')

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=uid)
        conf = Profile.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        conf = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        conf.is_confirmed = True
        user.save()
        conf.save()
        login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('dashboard')

    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('reActivation')


def setactive(request):
    if request.user.is_active:
        messages.success(request, 'Your account is active.')
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'Your account is active.')

                    else:
                        user.is_active = True
                        user.save()
                        login(request, user)
                        messages.success(request, 'Your account is activated.')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid login')
                    return redirect('setactive')
        else:
            form = LoginForm()
            return render(request, 'account/setactive.html', {'form': form})


def reActivation(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            messages.success(request, 'Your account already is active!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Your account is inactive!')
            return redirect('setactive')

    if request.method == 'POST':
        form = EmailUser(request.POST)

        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            conf = Profile.objects.get(user=user)
            if user is not None:
                if not conf.is_confirmed:
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
                    message = render_to_string('account/activate.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()

                    messages.success(request, 'Email was sended. Please confirm your email address to complete the registration.')
                    return redirect('reActivation')
                else:
                    messages.success(request, 'Your account already is confirmed!')
                    return redirect('login')
            else:
                messages.error(request, 'Error')
    else:
        form = EmailUser()
        return render(request, 'account/reActivation.html', {'form': form})



@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def settings(request):
    user = request.user


    try:
        facebook_login = user.social_auth.get(provider='facebook')

    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'account/settings.html', {
        'facebook_login': facebook_login,
        'twitter_login': twitter_login,
        'google_login': google_login,

        'can_disconnect': can_disconnect
    })



def password(request):
    if request.user.has_usable_password():
        passwordform = PasswordChangeForm
    else:
        passwordform = AdminPasswordChangeForm

    if request.method == 'POST':
        form = passwordform(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = passwordform(request.user)
    return render(request, 'account/password.html', {'form': form})

"""
def generate_password(request):
    password = User.objects.make_random_password()
    request.user.set_password(password)
"""


@login_required
def softdelete(request):
    if request.method == 'POST':
        form = RemoveUser(request.POST)

        if form.is_valid():
            rem = User.objects.get(username=form.cleaned_data['username'])
            if rem is not None:
                rem.is_active = False
                rem.save()
                messages.success(request, 'Your account is inactive for next 30 days, after will be deleted forever.')
                logout(request)
                return redirect('login')
            else:
                messages.error(request, 'Error')
                return render(request, 'account/softdelete.html', {'form': form})
    else:
        form = RemoveUser()
        return render(request, 'account/softdelete.html', {'form': form})


@login_required
def harddelete(request):

    if request.method == 'POST':
        form = RemoveUser(request.POST)

        if form.is_valid():
            rem = User.objects.get(username=form.cleaned_data['username'])
            if rem is not None:
                rem.delete()
                messages.success(request, 'Your account was deleted forever and ever!')
                return redirect('login')
            else:
                messages.error(request, 'Error')
    else:
        form = RemoveUser()

    return render(request, 'account/harddelete.html', {'form': form})


def terms(request):
    return render(request, 'account/terms.html', {'section': 'terms'})


def ppolice(request):
    return render(request, 'account/ppolice.html', {'section': 'ppolice'})


def helpAuthAlreadyAssociated(request):
    return render(request, 'account/helpAuthAlreadyAssociated.html', {'section': 'helpAuthAlreadyAssociated'})


def emailhelp(request):
    another_user = None
    if request.user.is_authenticated:
        messages.success(request, 'You already login!')
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmailUser(request.POST)

        if form.is_valid():
            another_user = User.objects.get(email=form.cleaned_data['email'])
            if not another_user.has_usable_password():
                another_user.password = User.objects.make_random_password()
                another_user.save()
    else:
        form = EmailUser()
    return render(request, 'account/emailhelp.html', {'form': form, 'another_user': another_user})


def newpass(request):
    another_user = None
    if request.user.is_authenticated:
        messages.success(request, 'You already login!')
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmailUser(request.POST)

        if form.is_valid():
            another_user = User.objects.get(email=form.cleaned_data['email'])
            if not another_user.has_usable_password():
                another_user.password = User.objects.make_random_password()
                another_user.save()
                messages.success(request, 'Your account get password. Please, use "fogot password".')
            else:
                messages.error(request, 'Your account already has password. Please contact admin for restore access.')
    else:
        form = EmailUser()
    return render(request, 'account/newpass.html', {'form': form, 'another_user': another_user})

