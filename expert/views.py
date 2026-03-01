from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone

from farmer.models import FarmerProfile, SoilAnalysis
from .models import (
    ExpertProfile, ConsultationSession, ExpertAdvice, CropPlan, 
    PestDiagnosis, ExpertReview, ConsultationMessage, ExpertAvailability, ResourceLibrary
)
from .forms import ExpertRegistrationForm, ExpertAdviceForm, ConsultationMessageForm, ExpertProfileUpdateForm, CustomUserCreationForm


def expert_register(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        expert_form = ExpertRegistrationForm(request.POST)
        
        if user_form.is_valid() and expert_form.is_valid():
            try:
                user = user_form.save()
                expert_profile = expert_form.save(commit=False)
                expert_profile.user = user
                expert_profile.save()
                
                login(request, user)
                messages.success(request, "Expert registration successful! Your profile is pending verification.")
                return redirect("expert:dashboard")
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            # Show form errors
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
            
            for field, errors in expert_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        user_form = CustomUserCreationForm()
        expert_form = ExpertRegistrationForm()
    
    return render(request, "expert/register.html", {
        "user_form": user_form,
        "expert_form": expert_form,
        "specialization_choices": ExpertProfile.SPECIALIZATION_CHOICES
    })


@login_required
def expert_dashboard(request):
    user = request.user
    try:
        expert = user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    # Get consultation requests
    pending_consultations = ConsultationSession.objects.filter(
        expert=expert, 
        status='requested'
    ).order_by('-created_at')
    
    # Get active consultations
    active_consultations = ConsultationSession.objects.filter(
        expert=expert, 
        status__in=['scheduled', 'in_progress']
    ).order_by('-created_at')
    
    # Get recent advice given
    recent_advices = ExpertAdvice.objects.filter(
        expert=expert
    ).order_by('-created_at')[:5]
    
    # Get statistics
    total_consultations = ConsultationSession.objects.filter(expert=expert).count()
    completed_consultations = ConsultationSession.objects.filter(
        expert=expert, 
        status='completed'
    ).count()
    
    context = {
        "expert": expert,
        "pending_consultations": pending_consultations,
        "active_consultations": active_consultations,
        "recent_advices": recent_advices,
        "total_consultations": total_consultations,
        "completed_consultations": completed_consultations,
        "pending_count": pending_consultations.count(),
    }
    
    return render(request, "expert/dashboard.html", context)


@login_required
def expert_consultations(request):
    user = request.user
    try:
        expert = user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    # Get filters
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    # Base queryset
    consultations = ConsultationSession.objects.filter(expert=expert)
    
    # Apply filters
    if status != 'all':
        consultations = consultations.filter(status=status)
    
    if search:
        from django.db.models import Q
        consultations = consultations.filter(
            Q(title__icontains=search) | 
            Q(farmer__user__username__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Order by creation date
    consultations = consultations.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(consultations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "expert": expert,
        "consultations": page_obj,
        "status_choices": ConsultationSession.STATUS_CHOICES,
        "current_status": status,
        "current_search": search,
    }
    
    return render(request, "expert/consultations.html", context)


@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(ConsultationSession, id=consultation_id)
    user = request.user
    
    is_expert = hasattr(user, 'expert_profile') and consultation.expert == user.expert_profile
    is_farmer = hasattr(user, 'farmer_profile') and consultation.farmer == user.farmer_profile
    
    if not (is_expert or is_farmer):
        messages.error(request, "You don't have permission to view this consultation.")
        if hasattr(user, 'expert_profile'):
            return redirect("expert:dashboard")
        return redirect("farmer:dashboard")

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            ConsultationMessage.objects.create(
                consultation=consultation,
                sender=user,
                message=message_text,
                is_expert=is_expert
            )
            messages.success(request, "Message sent!")
            return redirect("expert:consultation_detail", consultation_id=consultation.id)

    # Get messages
    messages_list = consultation.messages.all().order_by('created_at')
    
    # Get soil analysis
    soil_analysis = SoilAnalysis.objects.filter(farmer=consultation.farmer).order_by('-created_at').first() if not is_farmer else None

    context = {
        "consultation": consultation,
        "messages_list": messages_list,
        "is_expert": is_expert,
        "soil_analysis": soil_analysis,
    }
    
    return render(request, "expert/consultation_detail.html", context)


@login_required
def consultation_session(request, session_id):
    """View for the live video and chat consultation session."""
    consultation = get_object_or_404(ConsultationSession, id=session_id)
    user = request.user
    
    is_expert = hasattr(user, 'expert_profile') and consultation.expert == user.expert_profile
    is_farmer = hasattr(user, 'farmer_profile') and consultation.farmer == user.farmer_profile
    
    if not (is_expert or is_farmer):
        messages.error(request, "You don't have permission to join this session.")
        return redirect("expert:dashboard")

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            ConsultationMessage.objects.create(
                consultation=consultation,
                sender=user,
                message=message_text,
                is_expert=is_expert
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({"status": "success"})
            return redirect("expert:consultation_session", session_id=session_id)

    messages_list = consultation.messages.all().order_by('created_at')
    
    context = {
        "consultation": consultation,
        "messages_list": messages_list,
        "is_expert": is_expert,
        "other_user": consultation.farmer.user if is_expert else consultation.expert.user,
    }
    
    return render(request, "expert/session.html", context)


@login_required
def accept_consultation(request, consultation_id):
    consultation = get_object_or_404(ConsultationSession, id=consultation_id)
    try:
        expert = request.user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    if consultation.expert != expert or consultation.status != 'requested':
        messages.error(request, "Cannot accept this consultation.")
        return redirect("expert:dashboard")
    
    consultation.status = 'scheduled'
    consultation.scheduled_time = timezone.now()
    consultation.save()
    
    messages.success(request, "Consultation accepted successfully!")
    return redirect("expert:consultation_detail", consultation_id=consultation.id)


@login_required
def complete_consultation(request, consultation_id):
    consultation = get_object_or_404(ConsultationSession, id=consultation_id)
    try:
        expert = request.user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    if consultation.expert != expert:
        messages.error(request, "Cannot complete this consultation.")
        return redirect("expert:dashboard")
    
    consultation.status = 'completed'
    consultation.save()
    
    # Update expert's total consultations
    expert.total_consultations += 1
    expert.save()
    
    messages.success(request, "Consultation marked as completed!")
    return redirect("expert:dashboard")


@login_required
def create_expert_advice(request, consultation_id):
    consultation = get_object_or_404(ConsultationSession, id=consultation_id)
    try:
        expert = request.user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    if consultation.expert != expert:
        messages.error(request, "Cannot create advice for this consultation.")
        return redirect("expert:dashboard")
    
    if request.method == "POST":
        advice_type = request.POST.get("advice_type", "").strip()
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        recommendations = request.POST.get("recommendations", "").strip()
        follow_up_required = request.POST.get("follow_up_required") == 'on'
        follow_up_date = request.POST.get("follow_up_date", "")
        
        if advice_type and title and content:
            advice = ExpertAdvice.objects.create(
                consultation=consultation,
                expert=expert,
                farmer=consultation.farmer,
                advice_type=advice_type,
                title=title,
                content=content,
                recommendations=recommendations,
                follow_up_required=follow_up_required,
                follow_up_date=follow_up_date if follow_up_date else None
            )
            
            messages.success(request, "Expert advice created successfully!")
            return redirect("expert:consultation_detail", consultation_id=consultation.id)
        else:
            messages.error(request, "Please fill all required fields.")
    
    context = {
        "consultation": consultation,
        "advice_types": ExpertAdvice.ADVICE_TYPE,
    }
    
    return render(request, "expert/create_advice.html", context)


@login_required
def expert_availability(request):
    try:
        expert = request.user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    if request.method == "POST":
        # Clear existing availability
        ExpertAvailability.objects.filter(expert=expert).delete()
        
        # Create new availability for each day
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(days):
            is_available = request.POST.get(f"available_{i}") == 'on'
            start_time = request.POST.get(f"start_time_{i}", "")
            end_time = request.POST.get(f"end_time_{i}", "")
            
            if is_available and start_time and end_time:
                ExpertAvailability.objects.create(
                    expert=expert,
                    day_of_week=i,
                    start_time=start_time,
                    end_time=end_time,
                    is_available=True
                )
        
        messages.success(request, "Availability updated successfully!")
        return redirect("expert:availability")
    
    # Get current availability
    availability = {}
    for i in range(7):
        try:
            avail = ExpertAvailability.objects.get(expert=expert, day_of_week=i)
            availability[i] = avail
        except ExpertAvailability.DoesNotExist:
            availability[i] = None
    
    context = {
        "expert": expert,
        "availability": availability,
        "days": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
    
    return render(request, "expert/availability.html", context)


@login_required
def expert_profile(request):
    try:
        expert = request.user.expert_profile
    except AttributeError:
        messages.error(request, "Please login as an expert.")
        return redirect("farmer:login")
    
    if request.method == "POST":
        form = ExpertProfileUpdateForm(request.POST, instance=expert)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("expert:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpertProfileUpdateForm(instance=expert)
    
    # Get expert's reviews
    reviews = ExpertReview.objects.filter(expert=expert).order_by('-created_at')[:10]
    
    # Get expert's recent advice
    recent_advices = ExpertAdvice.objects.filter(expert=expert).order_by('-created_at')[:5]
    
    context = {
        "expert": expert,
        "form": form,
        "reviews": reviews,
        "recent_advices": recent_advices,
    }
    
    return render(request, "expert/profile.html", context)


@login_required
def browse_experts(request):
    experts = ExpertProfile.objects.filter(
        verification_status='verified',
        is_available=True
    ).order_by('-average_rating')
    
    # Pagination
    paginator = Paginator(experts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "experts": page_obj,
        "specializations": ExpertProfile.SPECIALIZATION_CHOICES,
    }
    
    return render(request, "expert/browse_experts.html", context)


@login_required
def request_consultation(request, expert_id):
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Only farmers can request consultations.")
        return redirect("farmer:login")
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        session_type = request.POST.get("session_type", "chat")
        
        if title and description:
            consultation = ConsultationSession.objects.create(
                farmer=farmer,
                expert=expert,
                title=title,
                description=description,
                session_type=session_type,
                fee=expert.consultation_fee
            )
            
            messages.success(request, f"Consultation request sent to {expert.user.username}!")
            return redirect("consumer:dashboard")
        else:
            messages.error(request, "Please fill all required fields.")
    
    context = {
        "expert": expert,
        "session_types": ConsultationSession.SESSION_TYPE,
    }
    
    return render(request, "expert/request_consultation.html", context)


@login_required
def expert_reviews(request, expert_id):
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    reviews = ExpertReview.objects.filter(expert=expert).order_by('-created_at')
    
    context = {
        "expert": expert,
        "reviews": reviews,
    }
    
    return render(request, "expert/reviews.html", context)
