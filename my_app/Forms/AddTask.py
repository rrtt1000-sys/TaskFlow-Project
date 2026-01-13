from django import forms
from my_app.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['Title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control', # מוסיף את העיצוב מה-CSS שלך
                    'style': 'color-scheme: dark;' # טיפ: גורם ללוח השנה עצמו להיות כהה
                },
                format='%Y-%m-%dT%H:%M' # פורמט שדיאנגו צריך כדי לקרוא את השדה נכון
            ),
        }