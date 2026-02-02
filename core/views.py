from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Person, Document, Meeting, Enrollment, TrainingSession, Training, Lead, Payment
from .forms import MeetingForm, EnrollmentForm, DocumentForm, TrainingForm, TrainingSessionForm, PersonForm, LeadForm, PaymentForm
from datetime import date
from django.db.models import Sum, Count

from .services import LeadQueryService
from django.db.models import Q

# ============= LEAD VIEWS =============

@login_required
def lead_list(request):
    # Base queryset
    leads = Lead.objects.all().order_by('-created_at')
    
    # Use Service for filtering
    leads = LeadQueryService.get_filtered_leads(leads, request.GET)

    # Context for Filters
    context = {
        'leads': leads,
        'search_query': request.GET.get('q', ''),
        'contact_source_choices': Lead.CONTACT_SOURCE_CHOICES,
        'lead_stage_choices': Lead.LEAD_STAGE_CHOICES,
        'education_background_choices': Lead.EDUCATION_BACKGROUND_CHOICES,
        'interest_type_choices': Lead.INTEREST_TYPE_CHOICES,
        'trainings': Training.objects.filter(is_active=True),
        
        # Current Applied Filters (for keeping dropdowns selected)
        'current_contact_source': request.GET.get('contact_source', ''),
        'current_lead_stage': request.GET.get('lead_stage', ''),
        'current_education_background': request.GET.get('education_background', ''),
        'current_interest_type': request.GET.get('interest_type', ''),
        'current_follow_up_today': request.GET.get('follow_up_today', ''),
        'current_profession': request.GET.get('profession', ''),
        'today': date.today(),
        "follow_up_today_active": request.GET.get("follow_up_today") == "yes",
        
        # Multi-select training filters
        'selected_interested_trainings': request.GET.getlist('interested_training'),
        'selected_potential_trainings': request.GET.getlist('potential_training'),
        'selected_previous_trainings': request.GET.getlist('previous_training'),
    }
    
    return render(request, 'core/lead/lead_list.html', context)

@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm()
    return render(request, 'core/lead/lead_form.html', {'form': form, 'title': 'Yeni Lead Ekle'})

@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    meetings = lead.meeting_set.all().order_by('-meeting_date')
    enrollments = lead.enrollment_set.all().order_by('-enrollment_date')
    documents = lead.document_set.all().order_by('-uploaded_at')
    payments = lead.payment_set.all().order_by('-payment_date')
    
    # Calculate totals
    total_price = sum(e.training_session.price or 0 for e in enrollments if e.training_session)
    total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_price - total_paid
    
    return render(request, 'core/lead/lead_detail.html', {
        'lead': lead,
        'meetings': meetings,
        'enrollments': enrollments,
        'documents': documents,
        'payments': payments,
        'total_price': total_price,
        'total_paid': total_paid,
        'balance': balance,
    })

@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'core/lead/lead_form.html', {'form': form, 'title': 'Lead Düzenle'})

@login_required
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        return redirect('lead_list')
    return render(request, 'core/confirm_delete.html', {'object': lead, 'title': 'Lead Sil'})

@login_required
def convert_lead_to_student(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST":
        LeadQueryService.convert_to_student(lead)
    return redirect("lead_detail", pk=lead_id)

# ============= LEAD RELATED VIEWS =============

@login_required
def add_enrollment_to_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.lead = lead
            enrollment.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = EnrollmentForm()
    return render(request, 'core/enrollment/enrollment_form.html', {'form': form, 'lead': lead})

@login_required
def add_document_to_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.lead = lead
            document.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = DocumentForm()
    return render(request, 'core/document/document_form.html', {'form': form, 'lead': lead})

@login_required
def add_payment_to_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.lead = lead
            payment.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = PaymentForm()
    return render(request, 'core/payment/payment_form.html', {'form': form, 'lead': lead})

@login_required
def meeting_create(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.lead = lead
            meeting.user = request.user
            meeting.save()
            return redirect('lead_detail', pk=lead.id)
    else:
        form = MeetingForm()
    return render(request, 'core/meeting/meeting_form.html', {'form': form, 'lead': lead})

@login_required
def meeting_update(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=meeting.lead.id)
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'core/meeting/meeting_form.html', {'form': form, 'lead': meeting.lead})

@login_required
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    lead_id = meeting.lead.id
    if request.method == 'POST':
        meeting.delete()
        return redirect('lead_detail', pk=lead_id)
    return render(request, 'core/confirm_delete.html', {'object': meeting, 'title': 'Toplantı Sil'})

@login_required
def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=enrollment.lead.id)
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'core/enrollment/enrollment_form.html', {'form': form, 'lead': enrollment.lead})

@login_required
def delete_enrollment(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    lead_id = enrollment.lead.id
    if request.method == 'POST':
        enrollment.delete()
        return redirect('lead_detail', pk=lead_id)
    return render(request, 'core/confirm_delete.html', {'object': enrollment, 'title': 'Kayıt Sil'})

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    lead_id = document.lead.id
    if request.method == 'POST':
        document.delete()
        return redirect('lead_detail', pk=lead_id)
    return render(request, 'core/confirm_delete.html', {'object': document, 'title': 'Belge Sil'})

@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    lead_id = payment.lead.id
    if request.method == 'POST':
        payment.delete()
        return redirect('lead_detail', pk=lead_id)
    return render(request, 'core/confirm_delete.html', {'object': payment, 'title': 'Ödeme Sil'})

# ============= TRAINING VIEWS =============

def training_list(request):
    query = request.GET.get('q')
    if query:
        trainings = Training.objects.filter(name__icontains=query, is_active=True)
    else:
        trainings = Training.objects.filter(is_active=True)
    return render(request, 'core/training/training_list.html', {'trainings': trainings, 'search_query': query})

def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'core/training/training_detail.html', {'training': training})

@login_required
def training_create(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'core/training/training_form.html', {'form': form, 'title': 'Yeni Eğitim Ekle'})

@login_required
def training_update(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm(instance=training)
    return render(request, 'core/training/training_form.html', {'form': form, 'title': 'Eğitim Düzenle'})

@login_required
def session_create(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.training = training
            session.save()
            return redirect('training_detail', pk=training.id)
    else:
        form = TrainingSessionForm(initial={'price': 0})
    return render(request, 'core/session/session_form.html', {'form': form, 'training': training})

@login_required
def session_update(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('training_detail', pk=session.training.id)
    else:
        form = TrainingSessionForm(instance=session)
    return render(request, 'core/session/session_form.html', {'form': form, 'training': session.training})

# ============= DASHBOARD / REPORTS =============

@login_required
def dashboard(request):
    teaching_sessions = TrainingSession.objects.filter(instructor=request.user, start_date__gte=date.today())
    
    context = {
        'teaching_sessions': teaching_sessions
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def reports(request):
    total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_students = Lead.objects.filter(lead_stage='converted').count()
    enrollment_by_training = Training.objects.annotate(total_students=Count('trainingsession__enrollment')).order_by('-total_students')
    
    context = {
        'total_revenue': total_revenue,
        'total_students': total_students,
        'enrollment_by_training': enrollment_by_training
    }
    return render(request, 'core/reports.html', context)

# ============= PERSON VIEWS (LEGACY - may be removed) =============

def person_list(request):
    query = request.GET.get('q')
    if query:
        people = Person.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query),
            is_active=True
        ).order_by('-created_at')
    else:
        people = Person.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'core/person/person_list.html', {'people': people, 'search_query': query})

def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'core/person/person_detail.html', {'person': person})

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'core/person/person_form.html', {'form': form, 'title': 'Yeni Kişi Ekle'})

@login_required
def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'core/person/person_form.html', {'form': form, 'title': 'Kişi Düzenle'})

@login_required
def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'core/confirm_delete.html', {'object': person, 'title': 'Kişi Sil'})