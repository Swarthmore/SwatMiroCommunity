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

# What is calling swatcontext? What is request? How is it used?
def swatcontext(request):
    "Returns context variables helpful for swarthmore's workflow."
    return {
            'authmethod': settings.AUTH_METHOD,
            'authnextpage': settings.CAS_REDIRECT_URL,
            'disqus_sso': get_disqus_sso(request),
            #'message': base64.b64encode(data),
            #'timestamp': int(time.time()),
            #'settings.DISQUS_SECRET_KEY': settings.DISQUS_SECRET_KEY,
            #'pub_key': settings.DISQUS_PUBLIC_KEY,
            #'sig': hmac.HMAC(settings.DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
            
    }

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
    # {{ template_variable }}
    return """<script type="text/javascript">
    var disqus_config = function() {
        console.log(this)
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
        
    }
    </script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=settings.DISQUS_PUBLIC_KEY,
    )
