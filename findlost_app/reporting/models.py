from django.db import models
from django.contrib.auth.models import User


class SightingReport(models.Model):
    """A volunteer's report of a possible sighting. See Report
    Section 5.8 and Appendix A.1."""

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sighting_reports')
    location = models.CharField(max_length=255)
    sighted_date = models.DateField()
    sighted_time = models.TimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='reports/')
    encoding = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Sighting #{self.id} at {self.location}'
