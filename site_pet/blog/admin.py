from django.contrib import admin
from blog.models import Publication
from django_summernote.admin import SummernoteModelAdmin

class PublicationAdmin(SummernoteModelAdmin):
	pass

admin.site.register(Publication, PublicationAdmin)