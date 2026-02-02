from django import forms
from .models import Document, Enrollment, Training, TrainingSession, Person, Meeting, Lead, Payment

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'city', 'district',
            'instagram_username', 'profession',
            'contact_source', 'education_background', 'interest_type', 'lead_stage',
            'interested_trainings', 'potential_trainings', 'previous_trainings',
            'next_follow_up', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'next_follow_up': forms.DateInput(attrs={'type': 'date'}),
            'interested_trainings': forms.CheckboxSelectMultiple(),
            'potential_trainings': forms.CheckboxSelectMultiple(),
            'previous_trainings': forms.CheckboxSelectMultiple(),
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'photo', 'notes', 'is_active']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_date', 'summary', 'private_note', 'follow_up_date']
        widgets = {
            'meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'summary': forms.Textarea(attrs={'rows': 3}),
            'private_note': forms.Textarea(attrs={'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'description', 'default_duration', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['start_date', 'end_date', 'instructor', 'price']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['training_session', 'status', 'instructor_note']
        widgets = {
            'instructor_note': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['training_session', 'amount', 'payment_date', 'payment_method', 'note']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
