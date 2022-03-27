from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.index, name='home-page'),
    path('room/<int:pk>/', views.room_view, name='room-page'),
    path('create/', views.create_room, name='create-room'),
    path('update/<int:pk>', views.update_room, name='update-room'),
    path('delete/<int:pk>', views.delete_room, name='delete-room'),
    path('delete_message/<int:pk>', views.delete_message, name='delete-message'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register')
]