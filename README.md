SwatMiroCommunity
=================

Swarthmore Miro Community

Installation
============

.. note:: There are a couple of things that this installation guide assumes:

	* That you have installed `Mercurial`_ and `Git`_ on your system.
	* That you have installed `Python`_ and `virtualenv`_ on your system.

    These are basic instructions for installing a copy of Miro Community for local development and testing. You will need to modify the installation for a production environment - for example, you will need to draw up a requirements file that describes your production environment, and you will need to use your own settings file.

.. _Mercurial: http://mercurial.selenic.com/
.. _Git: http://git-scm.com/
.. _Python: http://python.org
.. _virtualenv: http://pypi.python.org/pypi/virtualenv

Creating a virtualenv
+++++++++++++++++++++

First up, you'll want to create and activate a virtual environment somewhere on your computer::

    virtualenv testenv
    cd testenv
    source bin/activate


Installing Miro Community
+++++++++++++++++++++++++

.. note:: Miro Community Default Install instructions are found here:

	* https://mirocommunity.readthedocs.org/en/1.9.1/installation.html

Swarthmore Specific Install Instructions:
1.) Issue the following commands from the newly created virtualenv

	pip install -e git+git://github.com/pculture/mirocommunity.git@1.10.0#egg=mirocommunity --no-deps
	cd src/mirocommunity/test_mc_project
	pip install -r requirements.txt
	cd ../../..
	pip install -e git+https://<github-username>@github.com/Swarthmore/SwatMiroCommunity.git#egg=swatmirocommunity --no-deps
	cd src/swatmirocommunity/default_community
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

 
	


