from django import forms
from django.forms import ModelForm
from .models import Profile
from crispy_forms.helper import FormHelper


class ProfileListFormHelper(FormHelper):
    model = Profile
    form_tag = False


class JeffChenForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'city', 'state', 'country', 'job_title', 'company',
                  'profile_image']


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
