"""The matching engine that compares a new sighting report against all
open missing-person records. See Project Report Section 7.1.4 and
Appendix A.2 (run_matching)."""
from django.conf import settings
from django.utils import timezone
from registry.models import MissingPerson
from .models import MatchResult
from .utils import bytes_to_encoding, compare_faces


def run_matching(report):
    """UC-04: Run Face Matching. Compares `report` (a SightingReport
    instance with a saved encoding) against every OPEN MissingPerson
    record and creates a MatchResult for every candidate below the
    configured confidence threshold (Sec. 8.4)."""
    threshold = getattr(settings, 'MATCH_CONFIDENCE_THRESHOLD', 0.6)
    report_encoding = bytes_to_encoding(report.encoding)

    results = []
    candidates = MissingPerson.objects.filter(status='OPEN').exclude(encoding__isnull=True)

    for person in candidates:
        person_encoding = bytes_to_encoding(person.encoding)
        is_match, distance = compare_faces(person_encoding, report_encoding, threshold)
        if is_match:
            confidence = round(max(0.0, (1 - distance)) * 100, 2)
            match = MatchResult.objects.create(
                person=person,
                report=report,
                confidence_score=confidence,
                status='PENDING',
            )
            results.append(match)

    return results


def approve_match(match):
    """UC-05 (approve branch) + UC-06 trigger. See Report Sec. 7.3."""
    from notify.utils import send_match_notification

    match.status = 'VERIFIED'
    match.reviewed_at = timezone.now()
    match.save()

    match.person.status = 'MATCH_FOUND'
    match.person.save()

    send_match_notification(match)
    return match


def reject_match(match):
    """UC-05 (reject branch)."""
    match.status = 'REJECTED'
    match.reviewed_at = timezone.now()
    match.save()
    return match
