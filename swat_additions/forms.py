from django import forms
from django.db import models
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm, EmbedSubmitVideoForm, DirectLinkSubmitVideoForm, SubmitVideoFormBase
from localtv import models
from localtv.models import Video
from django.conf import settings
from haystack import connections
from django.db import transaction

	
def categoriesField():
	# Defines a categories field for SubmitVideoFormBase
	return forms.MultipleChoiceField(required=False, choices=catChoices(), widget=forms.CheckboxSelectMultiple(attrs={"class":"category-check"}),label="Categories (optional)", help_text=("You may optionally categorize this video."))

def catChoices():
	allCats = models.Category.objects.filter(site=settings.SITE_ID)
	return [(thisCat.id,thisCat.name) for thisCat in allCats] # LIST COMPREHENSIONS! :D
		
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
	
	def __init__(self, *args, **kwargs):
		super(CatScrapedSubmitVideoForm, self).__init__(*args, **kwargs)
		self.fields['categories'].choices = catChoices()
				
	def save(self, commit=True):
		instance = super(ScrapedSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance

class CatEmbedSubmitVideoForm(EmbedSubmitVideoForm):
	categories = categoriesField()
	
	def __init__(self, *args, **kwargs):
		super(CatEmbedSubmitVideoForm, self).__init__(*args, **kwargs)
		self.fields['categories'].choices = catChoices()
		
	def save(self, commit=True):
		instance = super(EmbedSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance
	
class CatDirectLinkSubmitVideoForm(DirectLinkSubmitVideoForm):
	categories = categoriesField()
	
	def __init__(self, *args, **kwargs):
		super(CatDirectLinkSubmitVideoForm, self).__init__(*args, **kwargs)
		self.fields['categories'].choices = catChoices()
				
	def save(self, commit=True):
		instance = super(DirectLinkSubmitVideoForm, self).save(commit=True)
		#Update the search index here 
		updateCatIndex(instance)
		return instance

class AlwaysActiveSubmitVideoFormBase(SubmitVideoFormBase):
    def __init__(self, *args, **kwargs):
        super(AlwaysActiveSubmitVideoFormBase, self).__init__(*args, **kwargs)
        self.request = request
        print "self.request:",request
        site_settings = SiteSettings.objects.get_current()

        # HACK for backwards-compatibility
		#         if 'thumbnail_url' in self.fields:
		#             self.fields['thumbnail'] = self.fields['thumbnail_url']
    
    def save(self, commit=True):
        instance = super(SubmitVideoFormBase, self).save(commit=True)
        print "instance:",instance
		# Checks for admin settings - is the body of the first if really necessary?
        if self.request.user.is_authenticated():
            self.instance.user = self.request.user
            self.instance.contact = self.request.user.email
            print "User is authenticated"
        if self.request.user_is_admin():
            print "User is admin"
            instance.status = Video.ACTIVE
        return instance
        	
        if 'website_url' in self.fields:
            # Then this was a form which required a website_url - i.e. a direct
            # file submission. TODO: Find a better way to mark this?
            instance.try_to_get_file_url_data()