from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic, View

from animals.middleware.request_user import get_current_user
from shelter.models import Animals
from users.models import ShelterUser
from .forms import AnimalsForm


class ShelterView:
    @staticmethod
    def is_admin(user):
        return 'admins' in (group.name.lower() for group in user.groups.all())

    @staticmethod
    def get_current_user_shelter():
        user = get_current_user()
        if user:
            return ShelterUser.objects.get(user=user).shelter


class ShelterCRUDView(ShelterView, LoginRequiredMixin, View):
    pass


class GuestsListView(ShelterView, generic.ListView):
    model = Animals
    context_object_name = 'guests_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        shelter = self.get_current_user_shelter()
        self.queryset = Animals.actual_objects.get_queryset().filter(shelter=shelter)
        return super().get(request, *args, **kwargs)


class GuestsDetailView(ShelterView, generic.DetailView):
    model = Animals
    context_object_name = 'guest'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        shelter = self.get_current_user_shelter()
        animal = Animals.actual_objects.get(id=kwargs['pk'], shelter=shelter)
        result.context_data['can_delete'] = self.is_admin(user=request.user)
        result.context_data['animal_form'] = AnimalsForm(instance=animal)
        return result


class GuestsCreateView(ShelterCRUDView):
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


class GuestsEditView(ShelterCRUDView):
    def get(self, request, animal_id):
        shelter = self.get_current_user_shelter()
        animal = Animals.actual_objects.get(id=animal_id, shelter=shelter)
        context = {
            'animal_form': AnimalsForm(instance=animal),
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)

    def post(self, request, animal_id=None):
        animal = None
        if animal_id:
            shelter = self.get_current_user_shelter()
            animal = Animals.actual_objects.get(id=animal_id, shelter=shelter)
        animal_form = AnimalsForm(request.POST, instance=animal)
        if animal_form.is_valid():
            animal.save()
            return HttpResponseRedirect(f'/view/{animal_id}/')
        context = {
            'animal_form': animal_form,
            'animal_id': animal_id,
        }
        return render(request, template_name='shelter/animals_edit.html', context=context)


class GuestsDelete(ShelterCRUDView):
    def post(self, request, animal_id):
        if self.is_admin(user=request.user):
            raise Http404('<h1>Page not found</h1>')
        shelter = self.get_current_user_shelter()
        animal = Animals.actual_objects.get(id=animal_id, shelter=shelter)
        animal.soft_delete()
        return HttpResponseRedirect('/')
