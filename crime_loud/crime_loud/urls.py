from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web_interface.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'register', 'web_interface.views.registerNewUser', name = 'registerNewUser'),
    url(r'login', 'web_interface.views.login', name = 'login'),
    url(r'imageUpload', 'web_interface.views.imageUpload', name = 'imageUpload'),
    url(r'audioUpload', 'web_interface.views.UploadAudio', name = 'upload_audio'),
    url(r'videoUpload', 'web_interface.views.UploadVideo', name = 'upload_video'),
    url(r'viewProfile', 'web_interface.views.viewProfile', name = 'viewProfile'),
    url(r'backHome', 'web_interface.views.backHome', name = 'backHome'),
    url(r'logout', 'web_interface.views.logout', name = 'logout'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




