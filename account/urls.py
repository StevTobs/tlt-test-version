from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name=''),
    path('my-login', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name='user-logout'),
    path('register', views.register, name='register'),
    
  
]