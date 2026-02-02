from django.contrib import admin
from django.utils import timezone
from .models import Person, Training, TrainingSession, Enrollment, Meeting, Document, Payment, Lead

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
    list_display = ('lead', 'training_session', 'status', 'enrollment_date')
    list_filter = ('status', 'training_session__start_date')
    search_fields = ('lead__first_name', 'lead__last_name', 'training_session__training__name')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('lead', 'user', 'meeting_date', 'summary')
    list_filter = ('meeting_date', 'user')
    search_fields = ('lead__first_name', 'lead__last_name', 'summary')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('lead', 'document_type', 'uploaded_at', 'file')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('lead__first_name', 'lead__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lead', 'training_session', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('lead__first_name', 'lead__last_name')

class FollowUpTodayFilter(admin.SimpleListFilter):
    title = "Bugün aranacaklar"
    parameter_name = "follow_up_today"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Bugün"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                next_follow_up=timezone.now().date()
            )
        return queryset

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "instagram_username",
        "contact_source",
        "lead_stage",
        "first_meeting_date",
        "second_meeting_date",
        "next_follow_up",
        "last_contact_date",
    )

    list_filter = (
        "contact_source",
        "lead_stage",
        "interest_type",
        "education_background",
        "interested_trainings",
        "potential_trainings",
        FollowUpTodayFilter,
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
        "instagram_username",
    )

    filter_horizontal = (
        "interested_trainings",
        "potential_trainings",
    )

    readonly_fields = (
        "first_meeting_date",
        "first_meeting_by",
        "second_meeting_date",
        "second_meeting_by",
        "last_contact_date",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": (
                ("first_name", "last_name"),
                ("phone", "email"),
                ("instagram_username", "city", "profession"),
            )
        }),
        ("Lead Info", {
            "fields": (
                "contact_source",
                "education_background",
                "interest_type",
                "lead_stage",
            )
        }),
        ("Trainings", {
            "fields": (
                "interested_trainings",
                "potential_trainings",
            )
        }),
        ("Meetings Summary", {
            "fields": (
                "first_meeting_date",
                "first_meeting_by",
                "second_meeting_date",
                "second_meeting_by",
                "last_contact_date",
            )
        }),
        ("Follow-up & Notes", {
            "fields": (
                "next_follow_up",
                "notes",
            )
        }),
    )

    ordering = ("-created_at",)
