from django import forms
from django.db import models
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm, SubmitVideoFormBase
from localtv import models
from localtv.models import Video
from django.conf import settings


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
		instance = super(SubmitVideoFormBase, self).save(commit=False)
		
		# Checks for admin settings
		if self.request.user.is_authenticated():
			self.instance.user = self.request.user
			self.instance.contact = self.request.user.email
		if self.request.user_is_admin():
			instance.status = Video.ACTIVE
	
		if 'website_url' in self.fields:
			# Then this was a form which required a website_url - i.e. a direct
			# file submission. TODO: Find a better way to mark this?
			instance.try_to_get_file_url_data()
	
		old_m2m = self.save_m2m
	
		def save_m2m():
			print "self.cleaned_data",self.cleaned_data
			
			# Saves the categories for display on video viewing page		
			if self.cleaned_data.get('categories'):
				instance.categories = self.cleaned_data['categories']
				print 'type(instance.categories):',instance.categories
				
				# More legwork for saving categories here
				
			old_m2m()
		print 'commit',commit
		if commit:
			instance.save()
			save_m2m()
			
		else:
			self.save_m2m = save_m2m
		return instance
		