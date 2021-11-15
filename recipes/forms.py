from django.forms import ModelForm
from django import forms
from django.contrib.postgres.fields import ArrayField


# from .models import Listing, Bid, Comment, Category
from .models import Listing, Comment, Category


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea(attrs={'rows':'1', 'cols':'50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    prep_time = forms.DurationField()
    cook_time = forms.DurationField()
    steps = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    image_url = forms.CharField(widget=forms.URLInput())



# class CreateListingForm(forms.Form):
#     title = forms.CharField(label="Title")
#     description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
#     bid = forms.CharField(widget=forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))
#     image_url = forms.CharField(widget=forms.URLInput())