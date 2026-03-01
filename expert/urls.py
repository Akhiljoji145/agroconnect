from django.urls import path
from . import views

app_name = "expert"

urlpatterns = [
    path("expert/register/", views.expert_register, name="register"),
    path("expert/dashboard/", views.expert_dashboard, name="dashboard"),
    path("expert/consultations/", views.expert_consultations, name="consultations"),
    path("expert/profile/", views.expert_profile, name="profile"),
    path("expert/availability/", views.expert_availability, name="availability"),
    path("expert/consultation/<int:consultation_id>/", views.consultation_detail, name="consultation_detail"),
    path('consultation/<int:session_id>/session/', views.consultation_session, name='consultation_session'),
    path("expert/consultation/<int:consultation_id>/accept/", views.accept_consultation, name="accept_consultation"),
    path("expert/consultation/<int:consultation_id>/complete/", views.complete_consultation, name="complete_consultation"),
    path("expert/consultation/<int:consultation_id>/advice/", views.create_expert_advice, name="create_advice"),
    path("expert/browse/", views.browse_experts, name="browse_experts"),
    path("expert/<int:expert_id>/reviews/", views.expert_reviews, name="expert_reviews"),
    path("expert/<int:expert_id>/request/", views.request_consultation, name="request_consultation"),
]
