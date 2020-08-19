from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):

    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={
            "placeholder": "Subject of Request"
        }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            "placeholder": "eg: dawn@dawn.com"
        }
    ))
    location_info = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            "rows": 3,
        }
    ))
    ticket_description = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            "rows": 8,
        }
    ))

    class Meta:
        model = Ticket
        fields = ['subject', 'username',
                  'email', 'user_department',
                  'request_type', 'location_info', 'ticket_description']


class TicketTrackForm(forms.Form):

    ticket_id = forms.CharField(label='Ticket ID', widget=forms.TextInput(
        attrs={
            "placeholder": "Ticket ID emailed to you"
        }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            "placeholder": "eg: dawn@dawn.com"
        }
    ))
