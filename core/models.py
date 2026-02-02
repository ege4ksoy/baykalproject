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
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_date = models.DateTimeField()
    summary = models.TextField()
    private_note = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Meeting with {self.lead} on {self.meeting_date}"

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


class Lead(models.Model):

    CONTACT_SOURCE_CHOICES = [
        ('instagram', 'Instagram'),
        ('website', 'Web Sitesi'),
        ('phone', 'Telefon'),
        ('email', 'E-posta'),
        ('reference', 'Referans'),
    ]

    EDUCATION_BACKGROUND_CHOICES = [
        ('educated', 'Tekstil Eğitimi Almış'),
        ('self_taught', 'Alaylı'),
        ('student', 'Öğrenci'),
        ('unknown', 'Bilinmiyor'),
    ]

    INTEREST_TYPE_CHOICES = [
        ('online', 'Online'),
        ('onsite', 'Yüz Yüze'),
        ('both', 'Her İkisi'),
    ]

    LEAD_STAGE_CHOICES = [
        ('new', 'Yeni Geldi'),
        ('contacted', 'İlk Görüşme Yapıldı'),
        ('interested', 'İlgili'),
        ('follow_up', 'Takip Edilecek'),
        ('converted', 'Kayıta Döndü'),
        ('lost', 'Kaybedildi'),
    ]

    # Kimlik
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    instagram_username = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=150, blank=True, null=True)

    # Lead bilgileri
    contact_source = models.CharField(max_length=20, choices=CONTACT_SOURCE_CHOICES)
    education_background = models.CharField(max_length=20, choices=EDUCATION_BACKGROUND_CHOICES)
    interest_type = models.CharField(max_length=20, choices=INTEREST_TYPE_CHOICES)
    lead_stage = models.CharField(max_length=20, choices=LEAD_STAGE_CHOICES, default='new')
    next_follow_up = models.DateField(null=True, blank=True)

    # Görüşme özetleri
    first_meeting_date = models.DateTimeField(null=True, blank=True)
    first_meeting_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="lead_first_meetings"
    )

    second_meeting_date = models.DateTimeField(null=True, blank=True)
    second_meeting_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="lead_second_meetings"
    )
    last_contact_date = models.DateTimeField(null=True, blank=True)

    # Eğitim ilgileri
    interested_trainings = models.ManyToManyField(
        "Training", related_name="interested_leads", blank=True
    )
    potential_trainings = models.ManyToManyField(
        "Training", related_name="potential_leads", blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    converted_person = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_lead"
    )
    converted_at = models.DateTimeField(null=True, blank=True)
    converted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_leads"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

