from django import forms

class ImageUploadForm(forms.Form):
    username = forms.CharField()
    pic = forms.ImageField()

class FeedAddForm(forms.Form):
    username = forms.CharField()
    content = forms.CharField()
    pic = forms.ImageField()