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
    url(r'takePhoto','web_interface.views.takePhoto', name='take_photo'),
    url(r'view_image/(?P<image_id>\d+)','web_interface.views.viewImage', name='view_image'),
    url(r'view_audio/(?P<audio_id>\d+)','web_interface.views.viewAudio', name='view_audio'),
    url(r'view_video/(?P<video_id>\d+)','web_interface.views.viewVideo', name='view_video'),
    url(r'^assign_image_case/(?P<image_id>\d+)/(?P<case_id>\d+)','web_interface.views.assignCaseImage', name='assign_image_case'),
    url(r'^assign_video_case/(?P<video_id>\d+)/(?P<case_id>\d+)','web_interface.views.assignCaseVideo', name='assign_image_case'),
    url(r'^assign_audio_case/(?P<audio_id>\d+)/(?P<case_id>\d+)','web_interface.views.assignCaseAudio', name='assign_audio_case'),
    url(r'^add_case','web_interface.views.addCase', name='add_case'),
    url(r'^delete','web_interface.views.deletePDE', name='delete_pde'),
    url(r'viewImage/(?P<image_id>\d+)','web_interface.views.viewImageJDY', name='view_image_JDY'),
    url(r'viewVideo/(?P<video_id>\d+)','web_interface.views.viewVideoJDY', name='view_video_JDY'),
    url(r'viewAudio/(?P<audio_id>\d+)','web_interface.views.viewAudioJDY', name='view_audio_JDY'),
    url(r'RegisterUser','web_interface.views.RegisterAuthorizedUser', name='register user')
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




