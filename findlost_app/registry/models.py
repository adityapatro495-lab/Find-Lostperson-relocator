from django.db import models
from django.contrib.auth.models import User


class MissingPerson(models.Model):
    """Core case record. See Project Report Section 5.8 (Database Schema)
    and Appendix A.1."""

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('MATCH_FOUND', 'Match Found'),
        ('CLOSED', 'Closed'),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missing_persons')
    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    last_seen_location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='missing_photos/')
    encoding = models.BinaryField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.status})'
