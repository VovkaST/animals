from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from shelter.models import Animals
from .forms import AnimalsForm


class GuestsListView(generic.ListView):
    model = Animals
    queryset = Animals.objects.filter(is_deleted=False)
    context_object_name = 'guests_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        result.context_data['can_create'] = False
        if request.user.username.lower() in ('admin', 'user'):
            result.context_data['can_create'] = True
        return result


class GuestsDetailView(generic.DetailView):
    model = Animals
    context_object_name = 'guest'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        animal = get_object_or_404(Animals, id=kwargs['pk'], is_deleted=False)
        result.context_data['can_edit'] = False
        result.context_data['can_delete'] = False
        result.context_data['animal_form'] = AnimalsForm(instance=animal)
        if request.user.username.lower() in ('admin', 'user'):
            result.context_data['can_edit'] = True
        if request.user.username.lower() == 'admin':
            result.context_data['can_delete'] = True
        return result


class GuestsCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'animal_form': AnimalsForm(),
        }
        return render(request, template_name='shelter/animals_create.html', context=context)

    def post(self, request):
        animal_form = AnimalsForm(request.POST)
        if animal_form.is_valid():
            Animals.objects.create(**animal_form.cleaned_data)
            return HttpResponseRedirect('/')
        return render(request, template_name='shelter/animals_create.html', context={'animal_form': animal_form})


class GuestsEditView(LoginRequiredMixin, View):
    def get(self, request, animal_id):
        animal = get_object_or_404(Animals, id=animal_id, is_deleted=False)
        context = {
            'animal_form': AnimalsForm(instance=animal),
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)

    def post(self, request, animal_id=None):
        animal = None
        if animal_id:
            animal = Animals.objects.get(id=animal_id)
        animal_form = AnimalsForm(request.POST, instance=animal)
        if animal_form.is_valid():
            animal.save()
            return HttpResponseRedirect(f'/view/{animal_id}/')
        context = {
            'animal_form': animal_form,
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)


class GuestsDelete(LoginRequiredMixin, View):
    def post(self, request, animal_id):
        if request.user.username.lower() != 'admin':
            raise Http404('<h1>Page not found</h1>')
        animal = Animals.objects.get(id=animal_id)
        animal.soft_delete()
        return HttpResponseRedirect('/')
