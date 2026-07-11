from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.match_review, name='match_review'),
    path('review/<int:match_id>/approve/', views.approve, name='approve_match'),
    path('review/<int:match_id>/reject/', views.reject, name='reject_match'),
]
