from django import forms
from .models import SightingReport


class SightingReportForm(forms.ModelForm):
    class Meta:
        model = SightingReport
        fields = ['location', 'sighted_date', 'sighted_time', 'photo']
        widgets = {
            'sighted_date': forms.DateInput(attrs={'type': 'date'}),
            'sighted_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image file must be smaller than 5 MB.')
        return photo
