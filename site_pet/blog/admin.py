from django.contrib import admin
from blog.models import Publication, MyPublication
from django_summernote.admin import SummernoteModelAdmin
from django.core.exceptions import ValidationError
from django import forms
from shutil import rmtree
import os

# class PublicationForm(forms.ModelForm):
#     class Meta:
#         model = Publication
#         fields = '__all__'

#     def clean(self):
#         import pdb; pdb.set_trace()
#         return self.cleaned_data

class PublicationAdmin(SummernoteModelAdmin):
    def get_queryset(self, request):
        return Publication.objects.all()

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.user = request.user.get_username()
            obj.save()
            thumb_path = obj.thumbnail.file.name
            new_thumb_path = os.path.join(os.path.dirname(os.path.dirname(thumb_path)), str(obj.id))
            os.rename(thumb_path, new_thumb_path)
            rmtree(os.path.dirname(thumb_path))
            obj.thumbnail = os.path.join('blog/thumbnails', str(obj.id))            
            obj.save()
        else:
            if obj.user != request.user.get_username():
                raise ValidationError('You can\t edit this')
            obj.save()

    def delete_model(self, request, obj):
        thumbnail_path = obj.thumbnail.file.name
        obj.delete()
        os.remove(thumbnail_path)

class MyPublicationAdmin(PublicationAdmin):
    def get_queryset(self, request):
        return MyPublication.objects.filter(user=request.user.get_username())


admin.site.register(MyPublication, MyPublicationAdmin)
admin.site.register(Publication, PublicationAdmin)
