from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_person, name='register_person'),
    path('register/success/<int:person_id>/', views.register_success, name='register_success'),
    path('dashboard/', views.case_dashboard, name='case_dashboard'),
    path('case/<int:person_id>/', views.case_detail, name='case_detail'),
]
