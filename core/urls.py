from django.urls import path
from django.contrib.auth import views as auth_views

from core.views import (Home)


urlpatterns = [
    #login view
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'),
        name='login'),
    # logout view
    path('logout/', auth_views.LogoutView.as_view(template_name='core/login.html'),
        name='logout'),
    # home view
    path('', Home.as_view(), name='home'),
]