

from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': f"{_('Search Here')}..."}))