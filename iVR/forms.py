from django import forms

# Update user profile picture
class ImageUploadForm(forms.Form):
    username = forms.CharField()
    pic = forms.ImageField()

# Post text feed
class FeedAddTextForm(forms.Form):
    username = forms.CharField()
    content = forms.CharField()

# Post text plus picture feed
class FeedAddTextPlusPictureForm(forms.Form):
    username = forms.CharField()
    content = forms.CharField()
    pic = forms.ImageField()