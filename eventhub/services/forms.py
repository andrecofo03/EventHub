from django import forms
from django.utils import timezone
from services.models import Event

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        label="Data e Ora"
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'max_capacity']
        labels = {
            'max_capacity': 'Capacità massima (lascia vuoto per illimitata)',
        }

    def clean_date(self):   
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("Data non valida")
        return date


class EditEventForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        label="Data e Ora"
    )

    class Meta:
        model = Event
        fields = ['date', 'description']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("Data non valida")
        return date