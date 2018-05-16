from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView, TemplateView
from site_pet import views
from django.conf.urls import handler400, handler403, handler404, handler500

handler400='site_pet.views.err400'
handler403='site_pet.views.err403'
handler404='site_pet.views.err404'
handler500='site_pet.views.err500'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/blog')),
    url(r'^admin/', admin.site.urls),
    url(r'^400/', views.err400),
    url(r'^403/', views.err403),
    url(r'^404/', views.err404),
    url(r'^500/', views.err500),
    url(r'^about/$', views.about,name='about'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^members/', include('members.urls')),
    url(r'^staff/', include('staff.urls')),
    url(r'^events/', include('events.urls')),
    url('^', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
