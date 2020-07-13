from django.urls import path
from .views import GuestsListView, GuestsDetailView

urlpatterns = [
    path('', GuestsListView.as_view(), name='guests_list'),
    path('<int:pk>/view', GuestsDetailView.as_view(), name='guest_detail_view'),
]
