from django.contrib import admin
from django.urls import path, include
from . import views  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include users app URLs
    path('', views.home, name='home'),  # Add a path for the root URL
]
