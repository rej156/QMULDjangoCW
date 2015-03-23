from django import forms
from social.models import Message

class MessageForm(forms.Form):
    text = forms.CharField(label='Type here to leave a message',
                           widget=forms.Textarea(attrs={'cols': 35, 'rows': 5}))
    CHOICES=[('0','Public'),('1','Private')]
    private = forms.ChoiceField(label='',initial=0,choices=CHOICES, widget=forms.RadioSelect())
