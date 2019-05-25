from django.urls import path

from . import views

app_name = 'images'


urlpatterns = [
    path('', views.image_list, name='list'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('create/', views.image_create, name='create'),
    path('add/', views.image_add, name='add'),
    path('detail/<int:id>/<slug:slug>/edit/', views.image_edit, name='edit'),
    path('detail/<int:id>/<slug:slug>/delete/', views.image_delete, name='delete'),
    # path('edit/', views.image_edit, name='edit'),
    path('like/', views.image_like, name='like'),
    # path('ranking/', views.image_ranking, name='ranking'),

]
