from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Person, Document, Meeting, Enrollment, TrainingSession, Training
from .forms import MeetingForm, EnrollmentForm, DocumentForm, TrainingForm, TrainingSessionForm, PersonForm
from datetime import date
from django.db.models import Sum, Count

from django.db.models import Q

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
    enrollments = person.enrollment_set.all()
    documents = person.document_set.all()
    meetings = person.meeting_set.all().order_by('-meeting_date')
    return render(request, 'core/person/person_detail.html', {
        'person': person,
        'enrollments': enrollments,
        'documents': documents,
        'meetings': meetings
    })


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'core/person/person_form.html', {'form': form, 'title': 'Yeni Kişi Ekle'})


@staff_member_required
def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'core/person/person_form.html', {'form': form, 'title': 'Yeni Kişi Ekle'})


@staff_member_required
def upload_document(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.person = person
            document.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = DocumentForm()
    
    return render(request, 'core/document/document_form.html', {'form': form, 'person': person})

@staff_member_required
def delete_document(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        document = Document.objects.get(person=person)
        document.delete()
        return redirect('person_detail', pk=person.id)
    else:
        form = DocumentForm()
    
    return render(request, 'core/document/document_form.html', {'form': form, 'person': person})


@staff_member_required
def enroll_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.person = person
            enrollment.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = EnrollmentForm()
    return render(request, 'core/enrollment/enrollment_form.html', {'form': form, 'person': person})

@staff_member_required
def update_enrollment(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.person = person
            enrollment.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = EnrollmentForm()
    return render(request, 'core/enrollment/enrollment_form.html', {'form': form, 'person': person})

def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    # sessions = training.trainingsession_set.all() # Assuming standard reverse relation
    return render(request, 'core/training/training_detail.html', {'training': training})

def training_list(request):
    query = request.GET.get('q')
    if query:
        trainings = Training.objects.filter(name__icontains=query, is_active=True)
    else:
        trainings = Training.objects.filter(is_active=True)
    return render(request, 'core/training/training_list.html', {'trainings': trainings, 'search_query': query})

@staff_member_required
def training_create(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'core/training/training_form.html', {'form': form, 'title': 'Yeni Eğitim Ekle'})

@staff_member_required
def training_update(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'core/training/training_form.html', {'form': form, 'title': 'Yeni Eğitim Ekle'})

@login_required
def dashboard(request):
    # If user is instructor, show their upcoming sessions
    teaching_sessions = TrainingSession.objects.filter(instructor=request.user, start_date__gte=date.today())
    
    context = {
        'teaching_sessions': teaching_sessions
    }
    return render(request, 'core/dashboard.html', context)

@staff_member_required
def reports(request):
    total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_students = Person.objects.filter(is_active=True).count()
    enrollment_by_training = Training.objects.annotate(total_students=Count('trainingsession__enrollment')).order_by('-total_students')
    
    context = {
        'total_revenue': total_revenue,
        'total_students': total_students,
        'enrollment_by_training': enrollment_by_training
    }
    return render(request, 'core/reports.html', context)

@staff_member_required
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
        form = TrainingSessionForm(initial={'price': 0}) # Default or calculate based on training
    return render(request, 'core/session/session_form.html', {'form': form, 'training': training})

@staff_member_required
def session_update(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('training_detail', pk=training.id)
    else:
        form = TrainingSessionForm(instance=training)
    return render(request, 'core/session/session_form.html', {'form': form, 'training': training})

@staff_member_required
def meeting_create(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.person = person
            meeting.user = request.user
            meeting.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = MeetingForm()
    return render(request, 'core/meeting/meeting_form.html', {'form': form, 'person': person})

@staff_member_required
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

@staff_member_required
def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'core/confirm_delete.html', {'object': person, 'title': 'Kişi Sil'})

@staff_member_required
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

@staff_member_required
def session_update(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            session.save()
            return redirect('training_detail', pk=session.training.id)
    else:
        form = TrainingSessionForm(instance=session)
    return render(request, 'core/session/session_form.html', {'form': form, 'training': session.training})

@staff_member_required
def meeting_update(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=meeting.person.id)
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'core/meeting/meeting_form.html', {'form': form, 'person': meeting.person})

@staff_member_required
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    person_id = meeting.person.id
    if request.method == 'POST':
        meeting.delete()
        return redirect('person_detail', pk=person_id)
    return render(request, 'core/confirm_delete.html', {'object': meeting, 'title': 'Toplantı Sil'})

@staff_member_required
def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=enrollment.person.id)
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'core/enrollment/enrollment_form.html', {'form': form, 'person': enrollment.person})

@staff_member_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    person_id = document.person.id
    if request.method == 'POST':
        document.delete()
        return redirect('person_detail', pk=person_id)
    return render(request, 'core/confirm_delete.html', {'object': document, 'title': 'Belge Sil'})

@staff_member_required
def meeting_update(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=person.id)
    else:
        form = MeetingForm(instance=person)
    return render(request, 'core/meeting/meeting_form.html', {'form': form, 'person': person})