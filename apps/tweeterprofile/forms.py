from django import forms

from .models import TweeterProfile

class TweeterProfileForm(forms.ModelForm):
    class Meta:
        model = TweeterProfile
        fields = ('avatar',)