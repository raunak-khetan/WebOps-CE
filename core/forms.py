# core/forms.py

from django import forms
from .models import CFARegistration

class CFARegistrationStep1Form(forms.ModelForm):
    class Meta:
        model = CFARegistration
        fields = ['full_name', 'age', 'email', 'phone_number', 'alternate_phone', 'college_id_card_link']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter age'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),

            'phone_number': forms.TextInput(attrs={'placeholder': '+91 |'}),
            'alternate_phone': forms.TextInput(attrs={'placeholder': '+91 |'}),
            'college_id_card_link': forms.URLInput(attrs={'placeholder': 'Google Drive link'}),
        }
