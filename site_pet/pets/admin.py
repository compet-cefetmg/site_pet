from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from pets.models import *
from utils.decimal_to_roman import write_roman 

class PetInline(admin.StackedInline):
    model = Pet
    can_delete = False
    verbose_name_plural = 'Pet Info'


class UserAdmin(BaseUserAdmin):
    inlines = (PetInline, )


class CampusAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		obj.roman_id = write_roman(obj.id)
		obj.save()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Course)
