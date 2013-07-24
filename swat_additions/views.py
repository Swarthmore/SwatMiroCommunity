# Create your views here.
# from django.views.generic import FormView
from swat_additions import forms
from localtv.submit_video.views import SubmitURLView, SubmitVideoView
from django.shortcuts import render_to_response
from django.template import RequestContext
from localtv import models
from django.conf import settings
from tagging.utils import parse_tag_input

class CatSubmitURLView(SubmitURLView):
	form_class = forms.CatSubmitURLForm
	template_name = "localtv/submit_video/cat_submit.html"
        
        
	def get_form(self, form_class):
		# Initialize the form with initial category values 
		urlCategories = self.kwargs['categories']
		return form_class(initial={'categories': urlCategories})
		
class CatSubmitVideoView(SubmitVideoView):
	categories_list = []
	
	def get(self, request, *args, **kwargs):
		print "self.form_class",self.form_class
		# Pulls in categories from request, and splits
		if "categories" in request.GET:
			temp_categories = request.GET["categories"].split('/')
			allCats = models.Category.objects.filter(site=settings.SITE_ID)
			self.categories_list = []
			for thisCat in allCats:
				if thisCat.slug in temp_categories:
					self.categories_list.append(thisCat.id)
		
			# for category in self.categories_list:
			#	print 'Category:',category
		return super(CatSubmitVideoView, self).get(request, *args, **kwargs)
	
	
	def get_initial(self):
		# Checks checkboxes
		initial = super(CatSubmitVideoView, self).get_initial()
		#print ("INITIAL?", request.GET)
		#print "CATEGORIES", self.categories_list
		initial.update({'categories': self.categories_list})
		return initial
		