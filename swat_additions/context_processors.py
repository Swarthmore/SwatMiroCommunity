"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""
import base64
import hashlib
import hmac
import simplejson
import time
from django.conf import settings
from django.contrib.auth.models import User
from localtv.playlists.models import Playlist, PlaylistItem
from localtv.models import SiteSettings

def swatcontext(request):
    "Returns context variables helpful for swarthmore's workflow."
    return {
            'authmethod': settings.AUTH_METHOD,
            'authnextpage': settings.CAS_REDIRECT_URL,
            'disqus_sso': get_disqus_sso(request),
            'playlists': get_playlists(request),
            'playlists_enabled': SiteSettings.objects.get_current().playlists_enabled,
    }

def get_playlists(request):
	site_settings = SiteSettings.objects.get_current()
	if site_settings.playlists_enabled:
		# showing playlists                                                                 
		if request.user.is_authenticated():
			if request.user_is_admin() or site_settings.playlists_enabled == 1:
				# user can add videos to playlists                                          
				return Playlist.objects.filter(user=request.user)
	return None
	
# user will be a dictionary containing information from the current session
def get_disqus_sso(request):

    
    if not request.user.is_authenticated():
		# User is not logged in, return without doing anything
		# Where are read-only comments handled?
        return "User: not logged in"
    else:
        # Get user data
        email = str(request.user.email)
        uname = str(request.user.username)
        id = request.user.id
        full_name = request.user.get_full_name()
        #return "Username:",uname,"Email:",email,"ID:",id
    
	
    # create a JSON packet of our data attributes
    data = simplejson.dumps({
        'id': id,
        'username': uname,
        'email': email,
    })
    
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())
    # generate our hmac signature
    sig = hmac.HMAC(settings.DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    
 
	# return a script tag to insert the sso message
    return """<script type="text/javascript">
    var disqus_config = function() {
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
        
    }
    </script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=settings.DISQUS_PUBLIC_KEY,
    )
