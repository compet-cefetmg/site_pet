from django.contrib import admin
from blog.models import Publication, MyPublication
from django_summernote.admin import SummernoteModelAdmin
from django.core.exceptions import ValidationError
from members.models import Member
from django import forms
from shutil import rmtree
import os

class PublicationAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'last_modification')

    def get_queryset(self, request):
        return Publication.objects.all()

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.user = request.user
            obj.save()
            thumb_path = obj.thumbnail.file.name
            new_thumb_path = os.path.join(os.path.dirname(os.path.dirname(thumb_path)), str(obj.id))
            os.rename(thumb_path, new_thumb_path)
            rmtree(os.path.dirname(thumb_path))
            obj.thumbnail = os.path.join('MyPublication/images', str(obj.id))        
            obj.save()
        else:
            if obj.user != request.user:
                raise ValidationError('You can\t edit this')
            obj.save()

    def delete_model(self, request, obj):
        thumbnail_path = obj.thumbnail.file.name
        obj.delete()
        os.remove(thumbnail_path)

class MyPublicationAdmin(PublicationAdmin):
    def get_queryset(self, request):
        return MyPublication.objects.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = Member.objects.filter(user=request.user)
        return super(MyPublicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MyPublication, MyPublicationAdmin)
admin.site.register(Publication, PublicationAdmin)
