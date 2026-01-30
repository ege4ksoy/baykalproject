from django.urls import path
from . import views

urlpatterns = [
    path('', views.person_list, name='person_list'),
    path('person/<int:pk>/', views.person_detail, name='person_detail'),
    path('person/<int:person_id>/enroll/', views.enroll_person, name='enroll_person'),
    path('person/<int:person_id>/upload/', views.upload_document, name='upload_document'),
    path('trainings/', views.training_list, name='training_list'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('trainings/create/', views.training_create, name='training_create'),
    path('training/<int:training_id>/add-session/', views.session_create, name='session_create'),
    path('person/create/', views.person_create, name='person_create'),
    path('person/<int:pk>/update/', views.person_update, name='person_update'),
    path('person/<int:pk>/delete/', views.delete_person, name='delete_person'),
    path('person/<int:person_id>/add-meeting/', views.meeting_create, name='meeting_create'),
    path('meeting/<int:pk>/update/', views.meeting_update, name='meeting_update'),
    path('meeting/<int:pk>/delete/', views.delete_meeting, name='delete_meeting'),
    path('training/<int:pk>/update/', views.training_update, name='training_update'),
    path('session/<int:pk>/update/', views.session_update, name='session_update'),
    path('enrollment/<int:pk>/update/', views.enrollment_update, name='enrollment_update'),
    path('document/<int:pk>/delete/', views.delete_document, name='delete_document'),
]
