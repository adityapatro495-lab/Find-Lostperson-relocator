from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, initial='VOLUNTEER')
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role': self.cleaned_data['role'],
                    'phone_number': self.cleaned_data.get('phone_number', ''),
                }
            )
        return user
