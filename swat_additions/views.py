# Create your views here.
# from django.views.generic import FormView
from swat_additions import forms
from localtv.submit_video.views import SubmitURLView, SubmitVideoView

class CatSubmitURLView(SubmitURLView):
	form_class = forms.CatSubmitURLForm
	template_name = "localtv/submit_video/cat_submit.html"
	
	def get_form(self, form_class):
		# Initialize the form with initial category values 
		urlCategories = self.kwargs['categories']
		return form_class(initial={'categories': urlCategories})
		
class CatSubmitVideoView(SubmitVideoView):
	form_class = forms.CatScrapedSubmitVideoForm
	
	def get_initial(self):
		initial = super(CatSubmitVideoView, self).get_initial()
		#print ("INITIAL?", request.GET)
		initial.update({
        	'categories': ['cats'],
        })
		return initial
"""
	def get_form(self, form_class):
		# Initialize the form with initial category values 
		print self.kwargs
		return form_class()
"""