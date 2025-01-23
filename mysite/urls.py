from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include("polls.urls")),#aplicacion encuestas
    path('admin/', admin.site.urls), #sitioadmin
    path('accounts/', include('django.contrib.auth.urls')),#autentificacion
]
