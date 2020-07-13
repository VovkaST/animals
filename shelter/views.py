from django.shortcuts import render
from django.views import generic

from shelter.models import Animals


class GuestsView(generic.ListView):
    model = Animals
