from django import forms
from my_app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    # שדות נוספים לפרופיל כפי שמופיע בדרישות (אזור אישי/הגדרות)
    phone_number = forms.CharField(max_length=20, label="phone number")
    address = forms.CharField(max_length=255, widget=forms.TextInput(), label="address", required=False)

    class Meta:
        model = User

        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # יצירת הפרופיל כחלק מהרישום
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data.get('address')
            )
        return user