from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & Reports
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    
    # Lead URLs
    path('', views.lead_list, name='lead_list'),
    path('leads/', views.lead_list, name='lead_list_alt'),
    path('leads/create/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/update/', views.lead_update, name='lead_update'),
    path('leads/<int:pk>/delete/', views.delete_lead, name='delete_lead'),
    path('leads/<int:lead_id>/convert/', views.convert_lead_to_student, name='lead_convert'),
    
    # Lead related URLs
    path('leads/<int:lead_id>/add-enrollment/', views.add_enrollment_to_lead, name='add_enrollment_to_lead'),
    path('leads/<int:lead_id>/add-document/', views.add_document_to_lead, name='add_document_to_lead'),
    path('leads/<int:lead_id>/add-payment/', views.add_payment_to_lead, name='add_payment_to_lead'),
    path('leads/<int:lead_id>/add-meeting/', views.meeting_create, name='meeting_create'),
    
    # Meeting URLs
    path('meeting/<int:pk>/update/', views.meeting_update, name='meeting_update'),
    path('meeting/<int:pk>/delete/', views.delete_meeting, name='delete_meeting'),
    
    # Enrollment URLs
    path('enrollment/<int:pk>/update/', views.enrollment_update, name='enrollment_update'),
    path('enrollment/<int:pk>/delete/', views.delete_enrollment, name='delete_enrollment'),
    
    # Document URLs
    path('document/<int:pk>/delete/', views.delete_document, name='delete_document'),
    
    # Payment URLs
    path('payment/<int:pk>/delete/', views.delete_payment, name='delete_payment'),
    
    # Training URLs
    path('trainings/', views.training_list, name='training_list'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('trainings/create/', views.training_create, name='training_create'),
    path('training/<int:pk>/update/', views.training_update, name='training_update'),
    path('training/<int:training_id>/add-session/', views.session_create, name='session_create'),
    path('session/<int:pk>/update/', views.session_update, name='session_update'),
    
    # Person URLs (Legacy - may be removed)
    path('persons/', views.person_list, name='person_list'),
    path('person/<int:pk>/', views.person_detail, name='person_detail'),
    path('person/create/', views.person_create, name='person_create'),
    path('person/<int:pk>/update/', views.person_update, name='person_update'),
    path('person/<int:pk>/delete/', views.delete_person, name='person_delete'),
]
