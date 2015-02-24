from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web_interface.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'register', 'web_interface.views.registerNewUser', name = 'registerNewUser'),
    url(r'login', 'web_interface.views.login', name = 'login'),
    url(r'imageUpload', 'web_interface.views.imageUpload', name = 'imageUpload')
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
