from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extends Django's built-in User with a FINDLOST-specific role.
    See Project Report Appendix G.1."""

    ROLE_CHOICES = [
        ('FAMILY', 'Family / Registering User'),
        ('VOLUNTEER', 'Volunteer'),
        ('ADMIN', 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VOLUNTEER')
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, created, **kwargs):
    """Safety net: guarantees every User has a profile even if created
    outside the registration view (e.g. via createsuperuser)."""
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={'role': 'ADMIN' if instance.is_superuser else 'VOLUNTEER'})
