from django import forms
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm, SubmitVideoFormBase
from localtv import models
from localtv.models import Video
from django.conf import settings

def categoriesField():
	# Defines a categories field for SubmitVideoFormBase
	# Possible error
	print '\ncategoriesField'
	allCats = models.Category.objects.filter(site=settings.SITE_ID)
	print 'allCats',allCats
	CAT_CHOICES = []
	for thisCat in allCats:
		print 'thisCat',thisCat
		CAT_CHOICES.append((thisCat.id,thisCat.name))
	print 'CAT_CHOICES',CAT_CHOICES
	print 'returned',forms.MultipleChoiceField(choices=CAT_CHOICES, widget=forms.CheckboxSelectMultiple()),'\n'
	return forms.MultipleChoiceField(required=False, choices=CAT_CHOICES, widget=forms.CheckboxSelectMultiple())

class CatSubmitURLForm(SubmitURLForm):
	"""Accepts submission of a URL with categories."""
	# This class is being created
	# print "CatSubmitURLForm(SubmitURLForm)" widget=forms.HiddenInput()
	categories = forms.CharField()

class CatScrapedSubmitVideoForm(ScrapedSubmitVideoForm):
	print "\nHELLO!"
	categories = categoriesField()
	print '\ncategories',categories
	def save(self, commit=True):
		print "SAVING VIDEO"
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
			print "save_m2m"
		# Saves the categories and tags for display on video viewing page
			if self.cleaned_data.get('tags'):		
				instance.tags = self.cleaned_data['tags']
				
			if self.cleaned_data.get('categories'):
				instance.categories = self.cleaned_data['categories']
				
			old_m2m()
		print 'commit',commit
		if commit:
			instance.save()
			save_m2m()
			
		else:
			self.save_m2m = save_m2m
		return instance
		