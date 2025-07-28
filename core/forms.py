
from django import forms
from .models import Head, Team, TeamMember
from django.forms import modelformset_factory


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Head
        fields = ['name', 'gender', 'phone_no', 'email', 'program_enrolled', 'institute_name', 'year_of_passing']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder' : 'Select Gender'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = [('', 'Select Gender')] + list(self.fields['gender'].choices)

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
        fields = ['name', 'phone_no', 'email', 'program_enrolled', 'gender', 'institute_name', 'year_of_passing']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Institute Name'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of Passing'}),
        }
        
        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Gender'})
        self.fields['gender'].choices = [('', 'Select Gender')] + list(self.fields['gender'].choices)

