from django.urls import re_path, path
from rest_framework.authtoken import views

from .views_api import APIAnimals

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    re_path(r'animals/(?P<pk>\d+)?', APIAnimals.as_view(), name='api_guests'),
    # path('animals/', APIAnimals.as_view(), name='api_guest_create'),
    # path('create/', GuestsCreateView.as_view(), name='api_guest_create'),
    # path('view/<int:pk>/', GuestsDetailView.as_view(), name='api_guest_detail_view'),
    # path('edit/<int:animal_id>/', GuestsEditView.as_view(), name='api_guest_edit'),
    # path('delete/<int:animal_id>/', GuestsDelete.as_view(), name='api_guest_delete'),
]
