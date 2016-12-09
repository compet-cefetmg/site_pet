from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from cefet.models import *
from utils.decimal_to_roman import write_roman 


class CampusAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.roman_id = write_roman(obj.id)
        obj.save()


class PetAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_campus')
    
    def course_name(self, obj):
        return obj.course.name

    def course_campus(self, obj):
        return obj.course.campus


class MyPetAdmin(PetAdmin):
    fields = ['description', 'start', 'photo']

    def get_queryset(self, request):
        return MyPet.objects.filter(id=request.user.pet.id)


admin.site.register(Course)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Pet, PetAdmin)
# admin.site.register(MyPet, MyPetAdmin)
