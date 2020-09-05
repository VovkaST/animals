from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from shelter.models import Animals
from .forms import AnimalsForm


class ShelterView:
    @staticmethod
    def is_user_in_group(user, group_name):
        return group_name in (group.name.lower() for group in user.groups.all())

    def is_admin(self, user):
        return self.is_user_in_group(user=user, group_name='admins')

    def is_user(self, user):
        return self.is_user_in_group(user=user, group_name='users')


class ShelterCRUDView(ShelterView, LoginRequiredMixin, View):
    pass


class GuestsListView(ShelterView, generic.ListView):
    model = Animals
    queryset = Animals.objects.filter(is_deleted=False)
    context_object_name = 'guests_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        result.context_data['can_create'] = any((self.is_admin(user=request.user), self.is_user(user=request.user)))
        return result


class GuestsDetailView(ShelterView, generic.DetailView):
    model = Animals
    context_object_name = 'guest'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        animal = get_object_or_404(Animals, id=kwargs['pk'], is_deleted=False)
        result.context_data['can_edit'] = any((self.is_admin(user=request.user), self.is_user(user=request.user)))
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


class GuestsDelete(ShelterCRUDView):
    def post(self, request, animal_id):
        if self.is_admin(user=request.user):
            raise Http404('<h1>Page not found</h1>')
        animal = Animals.objects.get(id=animal_id)
        animal.soft_delete()
        return HttpResponseRedirect('/')
