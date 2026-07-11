from django.contrib import admin
from .models import SightingReport


@admin.register(SightingReport)
class SightingReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'location', 'sighted_date', 'created_at')
    search_fields = ('location',)
