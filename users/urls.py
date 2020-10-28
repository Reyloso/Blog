from django.urls import path

from .views import (SuccesRegisterView, UserCreateView, NoPermissionsView)

urlpatterns = [
    # users urls
    path('user/register', UserCreateView.as_view(), name = 'register_user'),
    path('user/success', SuccesRegisterView.as_view(), name = 'success_register_user'),
    path('user/withoutpermissions', NoPermissionsView.as_view(), name = 'user_no_permissions'),
]