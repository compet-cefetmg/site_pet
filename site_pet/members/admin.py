from django.contrib import admin
from members.models import *
from django.core.exceptions import PermissionDenied
from django.conf import settings
from shutil import rmtree
import os

class MembersAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email')

    def get_queryset(self, request):
        return Member.objects.all()

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.user = request.user
            obj.save()
            if obj.photo:
                photo_path = obj.photo.file.name
                new_photo_path = os.path.join(os.path.dirname(os.path.dirname(photo_path)), str(obj.id))
                os.rename(photo_path,new_photo_path)
                rmtree(os.path.dirname(photo_path))
                obj.photo = os.path.join('members/photos', str(obj.id))
            obj.save()
        else:
            if obj.user != request.user:
                raise PermissionDenied
            obj.save()

    def delete_model(self, request, obj):
        photo_path = os.path.join(settings.MEDIA_ROOT, obj.photo.file.name)
        obj.delete()
        os.remove(photo_path)

class MyMembersAdmin(MembersAdmin):
    def get_queryset(self, request):
        return MyMember.objects.filter(user=request.user)

admin.site.register(MyMember, MyMembersAdmin)
admin.site.register(Member, MembersAdmin)
admin.site.register(MemberRole)
