from django import forms
from social.models import Message

class MessageForm(forms.Form):
    text = forms.CharField(label='lol')
    private = forms.IntegerField()
