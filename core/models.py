from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Training(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    default_duration = models.IntegerField(help_text="Duration in hours or days", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TrainingSession(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.training.name} ({self.start_date})"

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('potential', 'Potansiyel'),
        ('enrolled', 'Kayıtlı'),
        ('completed', 'Tamamladı'),
        ('dropped', 'Bıraktı'),
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='potential')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    attendance_rate = models.IntegerField(blank=True, null=True, help_text="Percentage")
    instructor_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.person} - {self.training_session}"

class Meeting(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_date = models.DateTimeField()
    summary = models.TextField()
    private_note = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Meeting with {self.person} on {self.meeting_date}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('certificate', 'Sertifika'),
        ('registration_form', 'Kayıt Formu'),
        ('payment_receipt', 'Dekont'),
        ('homework', 'Ödev'),
        ('photo', 'Fotoğraf'),
        ('other', 'Diğer'),
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_type} - {self.file.name}"

class Payment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.person} - {self.amount}"
