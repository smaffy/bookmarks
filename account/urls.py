from django.urls import path, include
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('newpass/', views.newpass, name='newpass'),

    # создать свои собственные представления, если нужно организовать другое поведение.
    # path('', include('django.contrib.auth.urls')),

    # registration (new user)
    path('register/', views.register, name='register'),

    # profile
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),

    # Privacy Policy and Terms and Conditions
    path('register/ppolice/', views.ppolice, name='ppolice'),
    path('register/terms/', views.terms, name='terms'),

    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),

    # exception AuthAlreadyAssociated
    path('helpAuthAlreadyAssociated/', views.helpAuthAlreadyAssociated, name='helpAuthAlreadyAssociated'),

    # delete acc
    path('delete/', views.softdelete, name='softdelete'),
    path('delete/harddelete/', views.harddelete, name='harddelete'),

    # activate account
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reActivation/', views.reActivation, name='reActivation'),
    path('setactive/', views.setactive, name='setactive'),

    # help with non unique email
    path('register/emailhelp/', views.emailhelp, name='emailhelp'),

    # view for profile list and details
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),

]
