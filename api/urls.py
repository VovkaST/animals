from django.urls import re_path, path
from rest_framework.authtoken import views

from .views import APIAnimals

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    re_path(r'animals/(?P<pk>\d+)?', APIAnimals.as_view(), name='api_guests'),
]
