from django import forms

class ImageUploadForm(forms.Form):
    pic = forms.ImageField()
    username = forms.CharField()