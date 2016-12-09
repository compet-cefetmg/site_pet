from django.contrib import admin
from blog.models import Post, MyPost
from django_summernote.admin import SummernoteModelAdmin
from django.core.exceptions import ValidationError
from members.models import Member
from django import forms
from shutil import rmtree
import os
from django.conf import settings


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'last_modification')

    def get_queryset(self, request):
        return Post.objects.all()

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.user = request.user
            obj.save()
            # thumbnail_path = obj.thumbnail.file.name
            # new_thumbnail_path = os.path.join('static/blog', str(obj.id))
            # os.rename(thumbnail_path, new_thumbnail_path)
            # rmtree(os.path.dirname(thumbnail_path))
            # obj.thumbnail = os.path.join('blog', str(obj.id))        
            # obj.save()
        else:
            if obj.user != request.user:
                raise ValidationError('You can\t edit this')
            obj.save()

    def delete_model(self, request, obj):
        thumbnail_path = obj.thumbnail.file.name
        obj.delete()
        os.remove(thumbnail_path)


class MyPostAdmin(PostAdmin):
    def get_queryset(self, request):
        return MyPost.objects.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = Member.objects.filter(user=request.user)
        return super(MyPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# admin.site.register(MyPost, MyPostAdmin)
# admin.site.register(Post, PostAdmin)
