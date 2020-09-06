from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Animals, ShelterUser, Shelter

admin.site.unregister(User)


class UserInline(admin.StackedInline):
    model = ShelterUser
    can_delete = False
    verbose_name_plural = 'Доп. информация'


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class ShelterUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'shelter']
    inlines = (UserInline,)

    def shelter(self, obj):
        shelter = ShelterUser.objects.filter(user=obj)
        if shelter.count():
            return shelter[0].shelter.title
    shelter.short_description = 'Приют'


admin.site.register(Animals)
