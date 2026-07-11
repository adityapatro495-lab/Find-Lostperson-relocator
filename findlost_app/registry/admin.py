from django.contrib import admin
from .models import MissingPerson


@admin.register(MissingPerson)
class MissingPersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'last_seen_location', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'last_seen_location')
