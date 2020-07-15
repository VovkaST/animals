from django.urls import path
from .views import GuestsListView, GuestsDetailView, GuestsCreateView, GuestsEditView, GuestsDelete

urlpatterns = [
    path('', GuestsListView.as_view(), name='guests_list'),
    path('create/', GuestsCreateView.as_view(), name='guest_create'),
    path('view/<int:pk>/', GuestsDetailView.as_view(), name='guest_detail_view'),
    path('edit/<int:animal_id>/', GuestsEditView.as_view(), name='guest_edit'),
    path('delete/<int:animal_id>/', GuestsDelete.as_view(), name='guest_delete'),  # TODO Пересмотреть...
]
