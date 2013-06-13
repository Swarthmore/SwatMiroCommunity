from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = ( 
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
    static(settings.UPLOADTEMPLATE_MEDIA_URL,document_root=settings.UPLOADTEMPLATE_MEDIA_ROOT)
)

if settings.AUTH_METHOD == 'cas':
    urlpatterns += (
        patterns('',
            url(r'^accounts/login/$', 'django_cas.views.login'),
            url(r'^accounts/logout/$', 'django_cas.views.logout'),
        )
    )
    
if settings.AUTH_METHOD == 'both':
    # TODO change template to present users with their login options
    # Seems like I add SSO login options here
    urlpatterns += (
        patterns('',
            url(r'^cas/login/$', 'django_cas.views.login'),
            url(r'^cas/logout/$', 'django_cas.views.logout'),
        )
    ) 
    
urlpatterns += (
    patterns('',
        url(r'^', include('localtv.contrib.contests.urls')),
        url(r'^', include('localtv.urls')),
    )  
)
