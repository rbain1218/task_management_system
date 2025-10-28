from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('home/', views.home_redirect, name='home_alt'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
]
