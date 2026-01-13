from django import forms

from my_app.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Team', 'role', 'address', 'phone_number']

        widgets = {
            'Team': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'כתובת מגורים'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'מספר טלפון'}),
        }
        labels = {
            'Team': 'בחר צוות',
            'role': 'מה התפקיד שלך?',
            'address': 'כתובת',
            'phone_number': 'טלפון',
        }