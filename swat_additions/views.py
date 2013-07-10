# Create your views here.
# from django.views.generic import FormView
from swat_additions import forms
from localtv.submit_video.views import SubmitURLView, SubmitVideoView
from django.shortcuts import render_to_response
from django.template import RequestContext

class CatSubmitURLView(SubmitURLView):
	form_class = forms.CatSubmitURLForm
	template_name = "localtv/submit_video/cat_submit.html"
        
        
	def get_form(self, form_class):
		# Initialize the form with initial category values 
		urlCategories = self.kwargs['categories']
		return form_class(initial={'categories': urlCategories})
		
class CatSubmitVideoView(SubmitVideoView):
	form_class = forms.CatScrapedSubmitVideoForm
	categories_list = []
	
	def get(self, request, *args, **kwargs):
		if "categories" in request.GET:
			self.categories_list = request.GET["categories"].split('/')
			for category in self.categories_list:
				print 'Category:',category
		return super(CatSubmitVideoView, self).get(request, *args, **kwargs)
		
	
	def get_initial(self):
		initial = super(CatSubmitVideoView, self).get_initial()
		#print ("INITIAL?", request.GET)
		#print "CATEGORIES", self.categories_list
		initial.update({
        	'categories': self.categories_list,
        })
		return initial
"""
	def get_form(self, form_class):
		# Initialize the form with initial category values 
		print self.kwargs
		return form_class()
"""