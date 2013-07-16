from django import forms
from django.db import models
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm, SubmitVideoFormBase
from localtv import models
from localtv.models import Video
from django.conf import settings
from haystack import connections
from haystack.management.commands import update_index


def categoriesField():
	# Defines a categories field for SubmitVideoFormBase
	# Possible error
	allCats = models.Category.objects.filter(site=settings.SITE_ID)
	CAT_CHOICES = [(thisCat.id,thisCat.name) for thisCat in allCats] # LIST COMPREHENSIONS! :D
	
	return forms.MultipleChoiceField(required=False, choices=CAT_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Video Categories")

class CatSubmitURLForm(SubmitURLForm):
	"""Accepts submission of a URL with categories."""
	# This class is being created
	# print "CatSubmitURLForm(SubmitURLForm)" 
	categories = forms.CharField(widget=forms.HiddenInput())

class CatScrapedSubmitVideoForm(ScrapedSubmitVideoForm):
	categories = categoriesField()
	
	def save(self, commit=True):
		instance = super(ScrapedSubmitVideoForm, self).save(commit=True)
		
		#Update the index here:
		instance._update_index = True
		index = connections['default'].get_unified_index().get_index(models.Video)
		index._enqueue_update(instance)
		#update_index.Command().handle(using='default')    
		return instance