from django import forms
from .models import MissingPerson


class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = ['name', 'age', 'gender', 'last_seen_location',
                  'contact_email', 'contact_phone', 'photo']
        widgets = {
            'last_seen_location': forms.TextInput(attrs={'placeholder': 'Street, Area, City'}),
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0 or age > 120:
            raise forms.ValidationError('Please enter a valid age.')
        return age

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image file must be smaller than 5 MB.')
        return photo
