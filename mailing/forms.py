from django import forms
from mailing.models import Sending, Subscriber, Message


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = ['message', 'start_time', 'end_time', 'subscribers', 'owner']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'subscribers': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'full_name', 'comment', 'owner']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['headline', 'body', 'owner']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }
