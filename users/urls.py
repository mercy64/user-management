from django.urls import path

from users.views import CustomUserManagement

urlpatterns = [
    path('create-user/', CustomUserManagement().create_user),
    path('delete-user/', CustomUserManagement().delete_user)
]