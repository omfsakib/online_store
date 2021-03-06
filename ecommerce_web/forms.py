from django import forms
from .models import *

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields =['email',]
    
class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields ='__all__'
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'