from django.db.models import Q
from django.utils import timezone
from .models import Lead

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

        # 3. ManyToMany Filters (Multi-select with AND logic)
        interested_trainings = params.getlist('interested_training')
        if interested_trainings:
            for training_id in interested_trainings:
                queryset = queryset.filter(interested_trainings__id=training_id)

        potential_trainings = params.getlist('potential_training')
        if potential_trainings:
            for training_id in potential_trainings:
                queryset = queryset.filter(potential_trainings__id=training_id)

        previous_trainings = params.getlist('previous_training')
        if previous_trainings:
            for training_id in previous_trainings:
                queryset = queryset.filter(previous_trainings__id=training_id)

        # 4. Profession Filter (text search)
        profession = params.get('profession')
        if profession:
            queryset = queryset.filter(profession__icontains=profession)

        # 5. Special Filters
        follow_up_today = params.get('follow_up_today')
        if follow_up_today == 'yes':
            today = timezone.now().date()
            queryset = queryset.filter(next_follow_up=today)

        return queryset.distinct()
    
    @staticmethod
    def convert_to_student(lead: Lead):
        """Lead'i öğrenci statüsüne dönüştür"""
        if lead.lead_stage == 'converted':
            return lead  # zaten dönüştürülmüş
        
        lead.lead_stage = "converted"
        lead.save()
        return lead
