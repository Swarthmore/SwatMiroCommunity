SwatMiroCommunity
=================

Swarthmore Miro Community

Installation:

Miro Community Default Install instructions are found here:
https://mirocommunity.readthedocs.org/en/1.9.1/installation.html

Swarthmore Install Instructions:
1.) Install virtual environment as instructed in the URL above.
2.) Issue the following commands from the newly created virtualenv

	pip install -e git+git://github.com/pculture/mirocommunity.git@1.9.1#egg=mirocommunity --no-deps
	pip install -e git+git://<username>@github.com/Swarthmore/SwatMiroCommunity.git
	cd src/SwatMiroCommunity/default_community
	pip install -r requirements.txt
  
3.) Create a file named secretkey.py in the directory /src/SwatMiroCommunity/default_community/default_community conating the following

	SECRET_KEY = "type_your_secret_key_here!"
	
4.) Setup the database and run the test server.

	python manage.py syncdb # This will prompt you to create an admin use. ***Important*** if you are going to use CAS authentication, use your Swarthmore user ID as the username
	python manage.py runserver


