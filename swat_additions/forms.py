from django import forms
from django.db import models
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm, EmbedSubmitVideoForm, DirectLinkSubmitVideoForm, SubmitVideoFormBase
from localtv import models
from localtv.models import Video
from django.conf import settings
from haystack import connections


def categoriesField():
	# Defines a categories field for SubmitVideoFormBase
	# Possible error
	allCats = models.Category.objects.filter(site=settings.SITE_ID)
	CAT_CHOICES = [(thisCat.id,thisCat.name) for thisCat in allCats] # LIST COMPREHENSIONS! :D
	return forms.MultipleChoiceField(required=False, choices=CAT_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"category-check"}), label="Categories (optional)", help_text=("You may optionally categorize this video."))
		
def updateCatIndex(instance):
	instance._update_index = True
	index = connections['default'].get_unified_index().get_index(models.Video)
	index._enqueue_update(instance)  
	
class CatSubmitURLForm(SubmitURLForm):
	"""Accepts submission of a URL with categories."""
	# This class is being created 
	categories = forms.CharField(required=False, widget=forms.HiddenInput())

class CatScrapedSubmitVideoForm(ScrapedSubmitVideoForm):
	categories = categoriesField()
		 
	def save(self, commit=True):
		instance = super(ScrapedSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance

class CatEmbedSubmitVideoForm(EmbedSubmitVideoForm):
	categories = categoriesField()
	
	def save(self, commit=True):
		instance = super(EmbedSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance
	
class CatDirectLinkSubmitVideoForm(DirectLinkSubmitVideoForm):
	categories = categoriesField()
	
	def save(self, commit=True):
		instance = super(DirectLinkSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance