from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View

from shelter.models import Animals
from .forms import AnimalsViewForm


class GuestsListView(generic.ListView):
    model = Animals
    context_object_name = 'guests_list'
    paginate_by = 10


class GuestsDetailView(generic.DetailView):
    model = Animals
    context_object_name = 'guest'


class GuestsEdit(View):
    def get(self, request, animal_id):
        animal = Animals.objects.get(id=animal_id)
        context = {
            'animal_form': AnimalsViewForm(instance=animal),
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)

    def post(self, request, animal_id):
        animal = Animals.objects.get(id=animal_id)
        animal_form = AnimalsViewForm(request.POST, instance=animal)
        if animal_form.is_valid():
            animal.save()
            return HttpResponseRedirect(f'/view/{animal_id}/')
        context = {
            'animal_form': animal_form,
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)


