from django import forms
from localtv.submit_video.forms import SubmitURLForm, ScrapedSubmitVideoForm
from localtv import models
from django.conf import settings

def categoriesField():
	allCats = models.Category.objects.filter(site=settings.SITE_ID)
	CAT_CHOICES = []
	for thisCat in allCats:
		CAT_CHOICES.append((thisCat.slug,thisCat.name))
	return forms.MultipleChoiceField(choices=CAT_CHOICES, widget=forms.CheckboxSelectMultiple())

class CatSubmitURLForm(SubmitURLForm):
	"""Accepts submission of a URL with categories."""
	categories = forms.CharField(widget=forms.HiddenInput())

class CatScrapedSubmitVideoForm(ScrapedSubmitVideoForm):
	categories = categoriesField()
	