from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from .models import MatchResult
from .engine import approve_match, reject_match


@login_required
@admin_required
def match_review(request):
    """UC-05: Verify Match. Administrator dashboard listing all
    pending candidate matches. See Report Section 7.3 / Figure 9.4."""
    pending_matches = MatchResult.objects.filter(status='PENDING')
    return render(request, 'matching/match_review.html', {'matches': pending_matches})


@login_required
@admin_required
def approve(request, match_id):
    match = get_object_or_404(MatchResult, id=match_id, status='PENDING')
    approve_match(match)
    return redirect('match_review')


@login_required
@admin_required
def reject(request, match_id):
    match = get_object_or_404(MatchResult, id=match_id, status='PENDING')
    reject_match(match)
    return redirect('match_review')
