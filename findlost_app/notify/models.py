from django.db import models
from matching.models import MatchResult


class Notification(models.Model):
    """Audit record of an email alert sent for a confirmed match.
    See Report Section 5.8 and Appendix A.1."""

    STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]

    match = models.ForeignKey(MatchResult, on_delete=models.CASCADE, related_name='notifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.match} ({self.status})'
