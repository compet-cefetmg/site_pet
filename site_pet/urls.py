from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/blog')),
    url(r'^admin/', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^members/', include('members.urls')),
    url(r'^staff/', include('staff.urls')),
    url('^', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
