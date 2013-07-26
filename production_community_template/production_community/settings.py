# Settings for production Miro Community on clips.swarthmore.edu

import os
import secretkey

_PROJECT_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

#------------ IMPORTANT SITE SPECIFIC VARIABLES ------------

# Set the MySQL database config varaibles
DB_NAME = "{dbname}"
DB_USER = "{dbuser}"
DB_PASSWORD = "{dbpassword}"

# Path to the homepage in the URL 
URL_PATH = "{urlpath}"

# Set to true to enable comments
COMMENTS_ENABLED = True

# Set the authentication method here options are:
# 'cas' = use CAS SSO login only
# 'private' = will use the auth from apache (will make entire site password protected)
# 'miro' = use the default Miro login
# 'both' = allow both cas and Miro (local) logins
AUTH_METHOD = '{authmethod}'

#------------ No need to edit below this line ---------------


DB = os.environ.get('DB')
# Force mysql in production
DB = 'mysql'
if DB == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',
        }
    }
elif DB == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mirocommunity_test',
            'USER': 'postgres',
            'TEST_CHARSET': 'utf8',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(_PROJECT_DIR, 'db_swat_default.sl3'),
        }
    }

# haystack search
SEARCH = os.environ.get('SEARCH')
# search still reverts to elasticsearch, look into this later.
if SEARCH == 'elasticsearch':
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://localhost:9200/',
            'PATH': os.path.join(_PROJECT_DIR, 'elasticsearch-0.90.1'),
            'INDEX_NAME': 'mirocommunity'
            }
        }
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(_PROJECT_DIR, 'whoosh_index'),
            }
        }

# ****IMPORTANT**** imported secret key from secretkey.py (file not included in GIT repo for security reasons)
SECRET_KEY = secretkey.SECRET_KEY

# (optional) required only if using 'cas' or 'both' authentication methods above
CAS_SERVER_URL = 'https://login.swarthmore.edu:8443/cas/'
CAS_REDIRECT_URL = '/'
CAS_VERSION = '2'

import djcelery
djcelery.setup_loader()
CELERY_TASK_SERIALIZER = 'json'
# Comment these lines out to use a celery server.
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(_PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = URL_PATH + '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(_PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = URL_PATH + '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(_PROJECT_DIR, '../../default_community/default_community/swat_miro_template/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'uploadtemplate.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
# 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware'
    'localtv.middleware.FixAJAXMiddleware',
    'localtv.middleware.UserIsAdminMiddleware',
)

if AUTH_METHOD == 'cas':
    MIDDLEWARE_CLASSES += ('django_cas.middleware.CASMiddleware',)

if AUTH_METHOD == 'private':
    MIDDLEWARE_CLASSES += ('django.contrib.auth.middleware.RemoteUserMiddleware',)
 
ROOT_URLCONF = 'default_community.urls'

UPLOADTEMPLATE_MEDIA_ROOT = MEDIA_ROOT + 'uploadtemplate/'
UPLOADTEMPLATE_MEDIA_URL = MEDIA_URL + 'uploadtemplate/'
UPLOADTEMPLATE_STATIC_ROOTS = [] # other directories which have static files
UPLOADTEMPLATE_TEMPLATE_ROOTS = [] # other directories with templates

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(_PROJECT_DIR, '../../default_community/default_community/swat_miro_template/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'localtv.contrib.contests',
    'localtv',
    'localtv.admin',
    'localtv.comments',
    'localtv.submit_video',
    'localtv.inline_edit',
    'localtv.user_profile',
    'localtv.playlists',
    'djvideo',
    'registration',
    'tagging',
    'uploadtemplate',
    'haystack',
    'email_share',
    'djcelery',
    'notification',
    'social_auth',
    'daguerre',
    'compressor',
    'mptt',
    'django_nose',
    'swat_additions',
)

if COMMENTS_ENABLED:
	INSTALLED_APPS += ('disqus',)
	# disqus keys
	DISQUS_PUBLIC_KEY = 'Rar4vj0zdEt4dQFtMHHZbHNQjAGUyeRWAv60mNJHfLqGvMh8R4uxmOhyJoo6JY8x'
	DISQUS_SECRET_KEY = 'i1nlbupybvKk5whgGuLIF0hTOc0bovjSVJiIz6ktqsZvGBUk9Jmv5Ai7qKmyHtbn'
	DISQUS_WEBSITE_SHORTNAME = 'swatmiro'
	
if os.environ.get('MIGRATIONS'):
    if 'south' not in INSTALLED_APPS:
        # South needs to come before django-nose for this to work correctly.
        INSTALLED_APPS = INSTALLED_APPS[:-1] + ('south',) + INSTALLED_APPS[-1:]
    SOUTH_TESTS_MIGRATE = True

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Webdriver test settings
#TEST_BROWSER = 'Firefox'
#TEST_RESULTS_DIR = os.path.join(_PROJECT_DIR, 'webdriver_results')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "localtv.context_processors.localtv",
    "localtv.context_processors.browse_modules",
    "localtv.contrib.contests.context_processors.contests",
    "swat_additions.context_processors.swatcontext"
)

# For debugging, don't redirect mistyped urls
APPEND_SLASH = True

LOGIN_REDIRECT_URL = URL_PATH + '/'

AUTHENTICATION_BACKENDS = (
    'localtv.auth_backends.MirocommunityBackend',
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.google.GoogleBackend',
)

if AUTH_METHOD == 'cas' or AUTH_METHOD == 'both':
    AUTHENTICATION_BACKENDS += ('django_cas.backends.CASBackend',)

if AUTH_METHOD == 'private':
    AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.RemoteUserBackend',)
    
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

AUTH_PROFILE_MODULE = 'user_profile.Profile'
COMMENTS_APP = 'localtv.comments'

FLOWPLAYER_SWF_URL = STATIC_URL + 'localtv/swf/flowplayer-3.2.5.swf'
FLOWPLAYER_JS_URL = STATIC_URL + 'localtv/js/extern/flowplayer-3.2.4.min.js'

CACHE_BACKEND = 'locmem://'

# vimeo keys
VIMEO_API_KEY = None
VIMEO_API_SECRET = None

# UStream key
USTREAM_API_KEY = None

# recaptcha keys
RECAPTCHA_PUBLIC_KEY = None
RECAPTCHA_PRIVATE_KEY = None

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7

# django-tagging
FORCE_LOWERCASE_TAGS = True

