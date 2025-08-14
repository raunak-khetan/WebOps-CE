
from django import forms
from .models import Head, Team, TeamMember, YEAR_CHOICES
from django.forms import modelformset_factory


# Using YEAR_CHOICES from models to keep a single source of truth

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Head
        fields = ['name', 'gender', 'phone_no', 'email', 'program_enrolled', 'institute_name', 'year_of_passing', 'is_disabled']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # Render gender as radio buttons; no placeholder option
            'gender': forms.RadioSelect(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_disabled': forms.RadioSelect(attrs={}),
        }
        
        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
            'is_disabled': 'Are you a person with disability (PwD)?',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure there is no blank placeholder like "---------" in radios
        self.fields['gender'].choices = [choice for choice in self.fields['gender'].choices if choice[0] != '']
        # Render graduating year as radios using static choices
        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES

class TeamName(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
        
        labels = {
            'team_name' : 'Team Name',
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'phone_no', 'email', 'program_enrolled', 'gender', 'institute_name', 'year_of_passing', 'is_disabled']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'gender-option'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Institute Name'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of Passing'}),
            'is_disabled': forms.RadioSelect(attrs={}),
        }
        
        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
            'is_disabled': 'Is this member a person with disability (PwD)?',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure consistent class and remove any blank placeholder choice
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].choices = [choice for choice in self.fields['gender'].choices if choice[0] != '']
        # Render graduating year as radios using static choices
        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES

