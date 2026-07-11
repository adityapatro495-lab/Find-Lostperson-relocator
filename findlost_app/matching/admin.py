from django.contrib import admin
from .models import MatchResult
from .engine import approve_match


@admin.action(description='Approve selected matches and notify contact')
def approve_selected(modeladmin, request, queryset):
    for match in queryset.filter(status='PENDING'):
        approve_match(match)


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('person', 'report', 'confidence_score', 'status', 'created_at')
    list_filter = ('status',)
    actions = [approve_selected]
