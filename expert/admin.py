from django.contrib import admin
from .models import (
    ExpertProfile, ConsultationSession, ExpertAdvice, CropPlan, 
    PestDiagnosis, ExpertReview, ConsultationMessage, ExpertAvailability, ResourceLibrary
)


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_years', 'verification_status', 'average_rating', 'is_available']
    list_filter = ['specialization', 'verification_status', 'is_available']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['average_rating', 'total_consultations', 'created_at', 'updated_at']
    actions = ['verify_experts', 'reject_experts']
    change_form_template = 'admin/expert/change_form.html'
    
    def verify_experts(self, request, queryset):
        """Admin action to verify selected experts"""
        count = queryset.update(verification_status='verified')
        self.message_user(request, f'{count} expert(s) successfully verified.')
    verify_experts.short_description = 'Verify selected experts'
    
    def reject_experts(self, request, queryset):
        """Admin action to reject selected experts"""
        count = queryset.update(verification_status='rejected')
        self.message_user(request, f'{count} expert(s) rejected.')
    reject_experts.short_description = 'Reject selected experts'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return self.readonly_fields + ['user']
        return self.readonly_fields
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            expert = ExpertProfile.objects.get(pk=object_id)
            extra_context['verification_documents'] = expert.verification_documents
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        """Override save to handle verification actions"""
        super().save_model(request, obj, form, change)
        
        # Handle verification actions from checkboxes
        if not change:  # Only on new objects
            return
            
        # Check for verification actions
        if 'auto_verify' in request.POST:
            obj.verification_status = 'verified'
            obj.save()
            self.message_user(request, f'Expert {obj.user.username} has been verified.')
        elif 'auto_reject' in request.POST:
            obj.verification_status = 'rejected'
            obj.save()
            self.message_user(request, f'Expert {obj.user.username} has been rejected.')


@admin.register(ConsultationSession)
class ConsultationSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer', 'expert', 'status', 'session_type', 'fee', 'created_at']
    list_filter = ['status', 'session_type', 'created_at']
    search_fields = ['title', 'farmer__user__username', 'expert__user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ExpertAdvice)
class ExpertAdviceAdmin(admin.ModelAdmin):
    list_display = ['title', 'expert', 'farmer', 'advice_type', 'follow_up_required', 'created_at']
    list_filter = ['advice_type', 'follow_up_required', 'created_at']
    search_fields = ['title', 'expert__user__username', 'farmer__user__username']
    readonly_fields = ['created_at']


@admin.register(CropPlan)
class CropPlanAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'expert', 'season', 'year', 'is_active', 'created_at']
    list_filter = ['season', 'year', 'is_active']
    search_fields = ['farmer__user__username', 'expert__user__username']
    readonly_fields = ['created_at']


@admin.register(PestDiagnosis)
class PestDiagnosisAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer', 'expert', 'affected_crop', 'severity', 'created_at']
    list_filter = ['severity', 'created_at']
    search_fields = ['title', 'farmer__user__username', 'expert__user__username', 'affected_crop']
    readonly_fields = ['created_at']


@admin.register(ExpertReview)
class ExpertReviewAdmin(admin.ModelAdmin):
    list_display = ['expert', 'farmer', 'rating', 'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = ['expert__user__username', 'farmer__user__username']
    readonly_fields = ['created_at']


@admin.register(ConsultationMessage)
class ConsultationMessageAdmin(admin.ModelAdmin):
    list_display = ['consultation', 'sender', 'is_expert', 'created_at']
    list_filter = ['is_expert', 'created_at']
    search_fields = ['consultation__title', 'sender__username']
    readonly_fields = ['created_at']


@admin.register(ExpertAvailability)
class ExpertAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['expert', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']
    search_fields = ['expert__user__username']


@admin.register(ResourceLibrary)
class ResourceLibraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'expert', 'resource_type', 'is_public', 'view_count', 'created_at']
    list_filter = ['resource_type', 'is_public', 'created_at']
    search_fields = ['title', 'expert__user__username', 'tags']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
