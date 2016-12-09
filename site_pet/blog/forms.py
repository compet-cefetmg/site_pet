from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Post
from django.core.exceptions import ObjectDoesNotExist
from django_summernote.widgets import SummernoteWidget


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'publish_as_team', 'text_call', 'text_content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_as_team': forms.RadioSelect(choices=[(True, 'Sim'), (False, 'Não')]),
            'text_call': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;'}),
            'text_content': SummernoteWidget(),
        }
