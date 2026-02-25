from django.contrib import admin
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import ExpertProfile, ConsultationSession, ExpertAdvice


@staff_member_required
def verification_dashboard(request):
    """Admin dashboard for expert verification management"""
    
    # Get verification statistics
    total_experts = ExpertProfile.objects.count()
    pending_experts = ExpertProfile.objects.filter(verification_status='pending').count()
    verified_experts = ExpertProfile.objects.filter(verification_status='verified').count()
    rejected_experts = ExpertProfile.objects.filter(verification_status='rejected').count()
    
    # Recent registrations (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_registrations = ExpertProfile.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Pending experts with details
    pending_experts_list = ExpertProfile.objects.filter(
        verification_status='pending'
    ).order_by('-created_at')[:10]
    
    # Recent verifications (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_verifications = ExpertProfile.objects.filter(
        updated_at__gte=seven_days_ago,
        verification_status__in=['verified', 'rejected']
    ).order_by('-updated_at')[:10]
    
    # Specialization breakdown
    specialization_stats = ExpertProfile.objects.values('specialization').annotate(
        count=Count('id'),
        pending=Count('id', filter=Q(verification_status='pending')),
        verified=Count('id', filter=Q(verification_status='verified'))
    ).order_by('-count')
    
    context = {
        'title': 'Expert Verification Dashboard',
        'total_experts': total_experts,
        'pending_experts': pending_experts,
        'verified_experts': verified_experts,
        'rejected_experts': rejected_experts,
        'recent_registrations': recent_registrations,
        'pending_experts_list': pending_experts_list,
        'recent_verifications': recent_verifications,
        'specialization_stats': specialization_stats,
        
        # Calculate percentages
        'pending_percentage': round((pending_experts / total_experts * 100) if total_experts > 0 else 0, 1),
        'verified_percentage': round((verified_experts / total_experts * 100) if total_experts > 0 else 0, 1),
        'rejected_percentage': round((rejected_experts / total_experts * 100) if total_experts > 0 else 0, 1),
    }
    
    return render(request, 'admin/expert_verification_dashboard.html', context)


# Customize admin site header
admin.site.site_header = 'AgroConnect Administration'
admin.site.site_title = 'AgroConnect Admin'
admin.site.index_title = 'Welcome to AgroConnect Admin'
