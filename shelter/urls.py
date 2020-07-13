from django.urls import path
from .views import GuestsView

urlpatterns = [
    path('', GuestsView.as_view(), name='guests'),
]
