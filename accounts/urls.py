from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('home/', views.home_redirect, name='home_alt'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
