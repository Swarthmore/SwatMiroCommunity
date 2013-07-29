from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from localtv.submit_video.views import can_submit_video, SubmitVideoView
from localtv.submit_video.forms import ScrapedSubmitVideoForm, EmbedSubmitVideoForm, DirectLinkSubmitVideoForm
from swat_additions.views import CatSubmitURLView, CatSubmitVideoView
from swat_additions.forms import CatScrapedSubmitVideoForm, CatEmbedSubmitVideoForm, CatDirectLinkSubmitVideoForm
                                       
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

if settings.AUTH_METHOD == 'private':
    urlpatterns += (
        patterns('',
            url(r'^accounts/login/$', 'django_cas.views.login'),
            url(r'^accounts/logout/$', 'swat_additions.views.swat_logout'),
        )
    )
    
if settings.AUTH_METHOD == 'both':
    # TODO change template to present users with their login options
    # Seems like I add SSO login options here
    urlpatterns += (
        patterns('',
            url(r'^cas/login/$', 'django_cas.views.login', name="cas_login_url"),
            url(r'^cas/logout/$', 'django_cas.views.logout', name="cas_logout_url"),
        )
    ) 

#lets pass the category name to the submission page
urlpatterns += (
	patterns('',
		url(r'^submit_video/categories/(?P<categories>[-\w/]+)+$', can_submit_video(CatSubmitURLView.as_view(
            scraped_url=reverse_lazy('localtv_submit_scraped_video'),
            direct_url=reverse_lazy('localtv_submit_directlink_video'),
            embed_url=reverse_lazy('localtv_submit_embedrequest_video'),
        )),
    	name='localtv_submit_video'), 
		url(r'^submit_video/scraped/$', can_submit_video(CatSubmitVideoView.as_view(
            submit_video_url=reverse_lazy('localtv_submit_video'),
            thanks_url_name='localtv_submit_thanks',
            form_class=CatScrapedSubmitVideoForm,
            template_name='localtv/submit_video/scraped.html',
            form_fields=('tags', 'categories', 'contact', 'notes'),
        )),
        name='localtv_submit_scraped_video'),
    url(r'^submit_video/embed/$', can_submit_video(CatSubmitVideoView.as_view(
            submit_video_url=reverse_lazy('localtv_submit_video'),
            thanks_url_name='localtv_submit_thanks',
            form_class=CatEmbedSubmitVideoForm,
            template_name='localtv/submit_video/embed.html',
            form_fields=('tags', 'categories', 'contact', 'notes', 'name', 'description',
                         'thumbnail_url', 'embed_code'),
        )),
        name='localtv_submit_embedrequest_video'),
    url(r'^submit_video/directlink/$', can_submit_video(CatSubmitVideoView.as_view(
            submit_video_url=reverse_lazy('localtv_submit_video'),
            thanks_url_name='localtv_submit_thanks',
            form_class=CatDirectLinkSubmitVideoForm,
            template_name='localtv/submit_video/direct.html',
            form_fields=('tags', 'categories', 'contact', 'notes', 'name', 'description',
                         'thumbnail_url', 'website_url'),
        )),
        name='localtv_submit_directlink_video'),
    )
)

urlpatterns += (
	
)

urlpatterns += (
    patterns('',
        url(r'^', include('localtv.contrib.contests.urls')),
        url(r'^', include('localtv.urls')),
        url(r'^help/$', 'swat_additions.views.help', name='localtv_help')
    )      
)

