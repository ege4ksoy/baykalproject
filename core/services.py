from django.db.models import Q
from django.utils import timezone
from .models import Lead, Person

class LeadQueryService:
    @staticmethod
    def get_filtered_leads(queryset, params):
        """
        Filters the Lead queryset based on dictionary parameters.
        Supported params:
        - q (search): name, phone, email, instagram
        - contact_source: exact match
        - lead_stage: exact match
        - education_background: exact match
        - interest_type: exact match
        - follow_up_today: 'yes' (checks next_follow_up date)
        """
        
        # 1. Search (Text)
        query = params.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(instagram_username__icontains=query)
            )

        # 2. Exact Filters
        contact_source = params.get('contact_source')
        if contact_source:
            queryset = queryset.filter(contact_source=contact_source)

        lead_stage = params.get('lead_stage')
        if lead_stage:
            queryset = queryset.filter(lead_stage=lead_stage)

        education_background = params.get('education_background')
        if education_background:
            queryset = queryset.filter(education_background=education_background)

        interest_type = params.get('interest_type')
        if interest_type:
            queryset = queryset.filter(interest_type=interest_type)

        # 3. Special Filters
        follow_up_today = params.get('follow_up_today')
        if follow_up_today == 'yes':
            today = timezone.now().date()
            queryset = queryset.filter(next_follow_up=today)

        return queryset
    
    @staticmethod
    def convert(lead: Lead, user):
        if lead.converted_person:
            return lead.converted_person  # tekrar dönüştürme yok

        person = Person.objects.create(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            city=lead.city,
            notes=lead.notes,
        )

        lead.converted_person = person
        lead.converted_at = timezone.now()
        lead.converted_by = user
        lead.lead_stage = "converted"
        lead.save()

        return person
