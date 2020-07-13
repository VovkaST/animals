from django.shortcuts import render
from django.views import generic

from shelter.models import Animals


class GuestsListView(generic.ListView):
    model = Animals
    context_object_name = 'guests_list'
    paginate_by = 10


class GuestsDetailView(generic.DetailView):
    model = Animals
    context_object_name = 'guest'
