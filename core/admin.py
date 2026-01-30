from django.contrib import admin
from .models import Person, Training, TrainingSession, Enrollment, Meeting, Document, Payment

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'city', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('is_active', 'city')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_duration', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('training', 'start_date', 'end_date', 'instructor', 'price')
    list_filter = ('start_date', 'instructor')
    search_fields = ('training__name',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('person', 'training_session', 'status', 'enrollment_date')
    list_filter = ('status', 'training_session__start_date')
    search_fields = ('person__first_name', 'person__last_name', 'training_session__training__name')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('person', 'user', 'meeting_date', 'summary')
    list_filter = ('meeting_date', 'user')
    search_fields = ('person__first_name', 'person__last_name', 'summary')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('person', 'document_type', 'uploaded_at', 'file')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('person__first_name', 'person__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('person', 'training_session', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('person__first_name', 'person__last_name')
