from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from farmer.models import FarmerProfile, SoilAnalysis


class ExpertProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('agronomist', 'Agronomist'),
        ('soil_scientist', 'Soil Scientist'),
        ('crop_specialist', 'Crop Specialist'),
        ('pest_management', 'Pest Management Expert'),
        ('irrigation_expert', 'Irrigation Expert'),
        ('market_analyst', 'Market Analyst'),
        ('organic_farming', 'Organic Farming Expert'),
        ('sustainability', 'Sustainability Expert'),
    ]
    
    
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expert_profile")
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES)
    qualifications = models.TextField(help_text="Educational qualifications and certifications")
    experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    bio = models.TextField(max_length=1000, help_text="Professional bio and expertise description")
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Fee per consultation session")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verification_documents = models.FileField(upload_to="expert_documents/", blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_consultations = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_specialization_display()}"

    def update_rating(self):
        reviews = ExpertReview.objects.filter(expert=self)
        if reviews:
            self.average_rating = sum(review.rating for review in reviews) / len(reviews)
        else:
            self.average_rating = 0
        self.save()


class ConsultationSession(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SESSION_TYPE = [
        ('chat', 'Chat Consultation'),
        ('video', 'Video Consultation'),
        ('report', 'Written Report'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="consultations")
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="consultations")
    title = models.CharField(max_length=200)
    description = models.TextField()
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE, default='chat')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation: {self.farmer} - {self.expert}"


class ExpertAdvice(models.Model):
    ADVICE_TYPE = [
        ('soil', 'Soil Analysis'),
        ('crop', 'Crop Planning'),
        ('pest', 'Pest Management'),
        ('irrigation', 'Irrigation'),
        ('market', 'Market Advisory'),
        ('general', 'General Advice'),
    ]
    
    consultation = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name="advices", null=True, blank=True)
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="advices")
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="expert_advices")
    soil_analysis = models.ForeignKey(SoilAnalysis, on_delete=models.SET_NULL, null=True, blank=True)
    advice_type = models.CharField(max_length=20, choices=ADVICE_TYPE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    recommendations = models.TextField(help_text="Specific recommendations for the farmer")
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advice: {self.title}"


class CropPlan(models.Model):
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('monsoon', 'Monsoon'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="crop_plans")
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="crop_plans")
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()
    primary_crops = models.TextField(help_text="List of primary crops recommended")
    rotation_plan = models.TextField(help_text="Crop rotation schedule")
    soil_preparation = models.TextField(blank=True)
    irrigation_plan = models.TextField(blank=True)
    fertilizer_recommendations = models.TextField(blank=True)
    expected_yield = models.TextField(blank=True)
    market_analysis = models.TextField(blank=True)
    implementation_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Crop Plan: {self.farmer} - {self.season} {self.year}"


class PestDiagnosis(models.Model):
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="pest_diagnoses")
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="pest_diagnoses")
    title = models.CharField(max_length=200)
    description = models.TextField()
    affected_crop = models.CharField(max_length=100)
    symptoms = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    diagnosis = models.TextField()
    treatment_recommendations = models.TextField()
    preventive_measures = models.TextField()
    chemical_treatments = models.TextField(blank=True, help_text="Chemical treatment options if needed")
    organic_alternatives = models.TextField(blank=True, help_text="Organic treatment options")
    estimated_damage = models.CharField(max_length=100, blank=True)
    recovery_time = models.CharField(max_length=50, blank=True)
    follow_up_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pest Diagnosis: {self.affected_crop}"


class PestDiagnosisImage(models.Model):
    diagnosis = models.ForeignKey(PestDiagnosis, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="pest_diagnosis/")
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ExpertReview(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="expert_reviews")
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="reviews")
    consultation = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(max_length=1000)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['farmer', 'consultation']

    def __str__(self):
        return f"Review: {self.farmer} - {self.expert} ({self.rating}/5)"


class ConsultationMessage(models.Model):
    consultation = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_expert = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.consultation.id}"


class ExpertAvailability(models.Model):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="availability")
    day_of_week = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['expert', 'day_of_week']

    def __str__(self):
        return f"Availability: {self.expert.user.username} - Day {self.day_of_week}"


class ResourceLibrary(models.Model):
    RESOURCE_TYPE = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('guide', 'Guide'),
        ('research', 'Research Paper'),
        ('tool', 'Tool/Calculator'),
    ]
    
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE)
    content = models.TextField()
    file_attachment = models.FileField(upload_to="expert_resources/", blank=True, null=True)
    external_link = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_public = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resource: {self.title}"
