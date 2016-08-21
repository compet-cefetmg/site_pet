from django.contrib import admin
from blog.models import Publication, MyPublication
from django_summernote.admin import SummernoteModelAdmin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms

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
        else:
            if obj.user != request.user.get_username():
                raise ValidationError('You can\t edit this')
        obj.save()

class MyPublicationAdmin(PublicationAdmin):
    def get_queryset(self, request):
        return MyPublication.objects.filter(user=request.user.get_username())


admin.site.register(MyPublication, MyPublicationAdmin)
admin.site.register(Publication, PublicationAdmin)