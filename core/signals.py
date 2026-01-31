from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Meeting


@receiver(post_save, sender=Meeting)
def update_lead_meeting_summary(sender, instance, created, **kwargs):
    if not created:
        return

    lead = instance.lead
    meetings = Meeting.objects.filter(lead=lead).order_by("meeting_date")

    count = meetings.count()

    if count == 1:
        lead.first_meeting_date = instance.meeting_date
        lead.first_meeting_by = instance.user
    elif count == 2:
        lead.second_meeting_date = instance.meeting_date
        lead.second_meeting_by = instance.user

    lead.last_contact_date = instance.meeting_date
    lead.save()
