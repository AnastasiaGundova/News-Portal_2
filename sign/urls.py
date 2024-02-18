from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('logout/confirm/',
         TemplateView.as_view(template_name='logout_confirm.html'),
         name='logout_confirm'),
    path('signup/',
         BaseRegisterView.as_view(template_name='accounts/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('index/',
         LoginView.as_view(template_name='protect/index.html'),
         name='index'),

]
