from django import forms

from .models import User, Website

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name',)

class WebsiteForm(forms.ModelForm):

    class Meta:
        model = Website
        fields = ('url',)