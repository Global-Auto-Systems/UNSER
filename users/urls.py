from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from .views import *


urlpatterns = [
	path('login_success/', user_views.login_success, name='login-success'),
	path('login/', auth_views.LoginView.as_view(template_name='ministry/base.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('register_sch/', user_views.register_school, name='register-school'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('upadte_profile/', user_views.updateprofile, name='update-profile'),


]
