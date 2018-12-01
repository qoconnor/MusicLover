from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

"""class EditProfileForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = (
            'description',
            'song',
            'album',
            'artist',
            'password',
        )"""

class EditProfileForm(forms.Form):
    description = forms.CharField(label='Bio:')
    song = forms.CharField(label='Favorite Song:')
    artist = forms.CharField(label='Favorite Artist:')
    album = forms.CharField(label='Favorite Album:')
