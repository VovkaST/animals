from django.urls import path
from .views import GuestsListView, GuestsDetailView, GuestsEdit

urlpatterns = [
    path('', GuestsListView.as_view(), name='guests_list'),
    path('add/', GuestsListView.as_view(), name='guest_new'),
    path('view/<int:pk>/', GuestsDetailView.as_view(), name='guest_detail_view'),
    path('edit/<int:animal_id>/', GuestsEdit.as_view(), name='guest_edit'),
]
