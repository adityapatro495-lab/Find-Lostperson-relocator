"""Email composition and dispatch for confirmed matches.
See Project Report Section 7.1.5 and Appendix A.4."""
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_match_notification(match):
    person = match.person
    subject = f'FINDLOST: Possible match found for {person.name}'
    message = (
        f'Dear Contact,\n\n'
        f'A potential sighting matching {person.name} has been verified '
        f'with {match.confidence_score:.1f}% confidence by our administration team.\n\n'
        f'Sighting location: {match.report.location}\n'
        f'Reported on: {match.report.sighted_date}\n\n'
        f'Please contact your nearest police station or the FINDLOST support '
        f'team immediately for further verification and assistance.\n\n'
        f'\u2014 The FINDLOST Team'
    )
    try:
        sent = send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            [person.contact_email], fail_silently=False,
        )
        status = 'SENT' if sent else 'FAILED'
    except Exception:
        status = 'FAILED'

    Notification.objects.create(match=match, status=status)
    return status
