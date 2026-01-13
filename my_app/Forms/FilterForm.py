from django import forms
from my_app.models import Task


class TaskFilterForm(forms.Form):
    worker = forms.CharField(
        required=False,
        label="סינון לפי עובד",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'הקלד שם עובד'
        })
    )

    status = forms.ChoiceField(
        required=False,
        label="סינון לפי סטטוס",
        choices=[('', 'כל הסטטוסים')] + list(Task.Status.choices),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )