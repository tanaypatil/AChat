from django import forms
from .models import *


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['user']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['user']
