from django.db import models


class Lead(models.Model):
    """Lead model to store generated lead information"""
    company_name = models.CharField(max_length=255, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    why_need_it = models.TextField(null=True, blank=True)
    outreach_message = models.TextField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    raw_response = models.TextField(null=True, blank=True)  # Full Gemini response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['industry', 'location']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.company_name} - {self.industry} ({self.location})"
