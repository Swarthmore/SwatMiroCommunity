SwatMiroCommunity
=================

Swarthmore Miro Community

Installation:
-------------

Miro Community Default Install instructions are found here:
https://mirocommunity.readthedocs.org/en/1.9.1/installation.html

Swarthmore Install Instructions:
1.) Install virtual environment as instructed in the URL above.
2.) Issue the following commands from the newly created virtualenv

	pip install -e git+git://github.com/pculture/mirocommunity.git@1.9.1#egg=mirocommunity --no-deps
	cd src
	git clone https://<github-username>@github.com/Swarthmore/SwatMiroCommunity.git
	cd SwatMiroCommunity/default_community
	pip install -r requirements.txt
  
3.) Create a file named secretkey.py in the directory /src/SwatMiroCommunity/default_community/default_community containing the following

	SECRET_KEY = "type_your_secret_key_here!"
	
4.) Setup the database and run the test server.

	python manage.py syncdb # This will prompt you to create an admin use. ***Important*** if you are going to use CAS authentication, use your Swarthmore user ID as the admin username
	python manage.py runserver
	
CAS Authentication Configuration:
---------------------------------

There are 3 possible authentication methods.  To set the method, change the AUTH_METHOD variable to one of the following:

	'miro' = (default if not set) use the default Miro login, authenticates from the Miro database
	'cas' = use CAS SSO login only
	'both' = allow both CAS and Miro (local) logins. A "Swarthmore Login" tab is added to the accounts/login/ page that triggers CAS authentication.

CAS_SERVER_URL settings:

	testing = 'https://idp.test.swarthmore.edu:8443/cas/'
	production = 'https://login.swarthmore.edu:8443/cas/'

 
	


