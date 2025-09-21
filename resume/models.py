from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s {self.title}"


class ResumeData(models.Model):
    """Structured data extracted from resume"""
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='data')
    full_text = models.TextField()  # Extracted text from resume
    contact_info = models.JSONField(default=dict)  # email, phone, address, etc.
    education = models.JSONField(default=list)  # List of education entries
    experience = models.JSONField(default=list)  # List of work experience
    skills = models.JSONField(default=list)  # Extracted skills
    certifications = models.JSONField(default=list)  # Certifications
    languages = models.JSONField(default=list)  # Programming/spoken languages
    projects = models.JSONField(default=list)  # Projects mentioned
    keywords = models.JSONField(default=list)  # Important keywords found
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Data for {self.resume.title}"


class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    overall_score = models.FloatField(default=0.0)
    keyword_matches = models.JSONField(default=dict)
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    job_fit_score = models.FloatField(default=0.0)  # 0-100 job fit score
    skills_match = models.JSONField(default=list)  # Matched skills with confidence
    suggested_changes = models.JSONField(default=list)  # Specific suggestions
    ats_score = models.FloatField(default=0.0)  # ATS compatibility score
    readability_score = models.FloatField(default=0.0)  # Resume readability
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.resume.title}"


class JobMatch(models.Model):
    resume_analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='job_matches')
    job_title = models.CharField(max_length=200)
    match_percentage = models.FloatField()
    missing_requirements = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.job_title} - {self.match_percentage}% match"
