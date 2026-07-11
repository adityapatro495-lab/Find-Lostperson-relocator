from django.db import models
from registry.models import MissingPerson
from reporting.models import SightingReport


class MatchResult(models.Model):
    """Output of the matching engine, pending admin verification.
    See Report Section 5.8 and Appendix A.1."""

    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='match_results')
    report = models.ForeignKey(SightingReport, on_delete=models.CASCADE, related_name='match_results')
    confidence_score = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-confidence_score']

    def __str__(self):
        return f'{self.person.name} <-> Report #{self.report.id} ({self.confidence_score:.1f}%)'
