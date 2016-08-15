from django import forms

class ImageUploadForm(forms.Form):
    username = forms.CharField()
    pic = forms.ImageField()

class FeedAddTextForm(forms.Form):
    username = forms.CharField()
    content = forms.CharField()

class FeedAddTextPlusPictureForm(forms.Form):
    username = forms.CharField()
    content = forms.CharField()
    pic = forms.ImageField()