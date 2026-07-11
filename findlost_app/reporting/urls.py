from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_report, name='submit_report'),
    path('success/<int:report_id>/', views.report_success, name='report_success'),
]
