from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator

from consumer.models import ConsumerProfile
from expert.models import ExpertProfile, ExpertAdvice, ConsultationSession
from supplier.models import SupplierProfile
from .models import FarmerProfile, FarmerPost, InventoryItem, MarketOrder, Product, SoilAnalysis, FarmerChatMessage


def home(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"DEBUG: User logged in: {user.username}")
            print(f"DEBUG: User has farmer_profile: {hasattr(user, 'farmer_profile')}")
            print(f"DEBUG: User has consumer_profile: {hasattr(user, 'consumer_profile')}")
            print(f"DEBUG: User has expert_profile: {hasattr(user, 'expert_profile')}")
            print(f"DEBUG: User has supplier_profile: {hasattr(user, 'supplier_profile')}")
            
            login(request, user)
            if hasattr(user, "farmer_profile"):
                return redirect("farmer:dashboard")
            if hasattr(user, "consumer_profile"):
                return redirect("consumer:dashboard")
            if hasattr(user, "expert_profile"):
                return redirect("expert:dashboard")
            if hasattr(user, "supplier_profile"):
                return redirect("supplier:dashboard")
            messages.error(request, "Account role not found. Please register.")
            return redirect("farmer:login")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("farmer:home")


def farmer_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        farm_name = request.POST.get("farm_name", "").strip()
        location = request.POST.get("location", "").strip()
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'farmer'
            user.save()
            FarmerProfile.objects.create(user=user, farm_name=farm_name, location=location)
            login(request, user)
            return redirect("farmer:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "farmer/register.html", {"form": form})


@login_required
def farmer_dashboard(request):
    user = request.user
    if not hasattr(user, "farmer_profile"):
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")

    farmer = user.farmer_profile

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "soil_analysis":
            ph_val = float(request.POST.get("ph") or 0)
            
            health_score = ""
            if ph_val < 6.5:
                health_score = "Acid Nature"
            elif ph_val <= 7.5:
                health_score = "Neutral"
            else:
                health_score = "Alkaline Nature"
                
            SoilAnalysis.objects.create(
                farmer=farmer,
                ph=ph_val,
                moisture=request.POST.get("moisture") or 0,
                temperature=request.POST.get("temperature") or 0,
                nitrogen=request.POST.get("nitrogen") or None,
                phosphorus=request.POST.get("phosphorus") or None,
                potassium=request.POST.get("potassium") or None,
                health_score=health_score
            )
            messages.success(request, "Soil analysis saved.")
            return redirect("farmer:dashboard")
        if form_type == "post_feed":
            description = request.POST.get("description", "").strip()
            image = request.FILES.get("image")
            if description:
                FarmerPost.objects.create(farmer=farmer, description=description, image=image)
                messages.success(request, "Post uploaded.")
                return redirect("farmer:dashboard")
        if form_type == "add_product":
            supplier_id = request.POST.get("supplier_id")
            supplier = None
            if supplier_id:
                try:
                    supplier = SupplierProfile.objects.get(id=supplier_id, is_active=True)
                except SupplierProfile.DoesNotExist:
                    pass

            Product.objects.create(
                farmer=farmer,
                supplier=supplier,
                name=request.POST.get("name", "").strip(),
                description=request.POST.get("description", "").strip(),
                price=request.POST.get("price") or 0,
                quantity=request.POST.get("quantity") or 0,
            )
            messages.success(request, "Product added.")
            return redirect("farmer:dashboard")
        if form_type == "add_inventory":
            InventoryItem.objects.create(
                farmer=farmer,
                name=request.POST.get("name", "").strip(),
                quantity=request.POST.get("quantity") or 0,
                unit=request.POST.get("unit", "unit").strip() or "unit",
            )
            messages.success(request, "Inventory item added.")
            return redirect("farmer:dashboard")
        
        if form_type == "community_chat":
            message_text = request.POST.get("message", "").strip()
            document = request.FILES.get("document")
            if message_text or document:
                FarmerChatMessage.objects.create(
                    farmer=farmer,
                    message=message_text,
                    document=document
                )
            return redirect("farmer:dashboard")

    analyses = SoilAnalysis.objects.filter(farmer=farmer).order_by("-created_at")[:5]
    posts = FarmerPost.objects.filter(farmer=farmer).order_by("-created_at")[:10]
    products = Product.objects.filter(farmer=farmer).order_by("-created_at")
    inventory = InventoryItem.objects.filter(farmer=farmer).order_by("-updated_at")
    chat_messages = FarmerChatMessage.objects.order_by("created_at")
    consultations = ConsultationSession.objects.filter(farmer=farmer).order_by("-created_at")

    context = {
        "farmer": farmer,
        "analyses": analyses,
        "posts": posts,
        "products": products,
        "inventory": inventory,
        "chat_messages": chat_messages,
        "consultations": consultations,
        "suppliers": SupplierProfile.objects.filter(is_active=True, is_verified=True),
        "recommendations": [
            "Maize and sorghum are suitable for current soil nutrients.",
            "Consider drip irrigation for moisture optimization.",
            "Monitor weather for rainfall in the next 7 days.",
        ],
    }
    return render(request, "farmer/dashboard.html", context)


@login_required
def browse_experts(request):
    """Browse and search for agricultural experts"""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")
    
    # Get filter parameters
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    verified_only = request.GET.get('verified', 'off')
    search_query = request.GET.get('search', '')
    
    # Filter experts
    experts = ExpertProfile.objects.filter(is_available=True)
    
    # Apply filters
    if specialization:
        experts = experts.filter(specialization=specialization)
    
    if location:
        experts = experts.filter(location__icontains=location)
    
    if verified_only == 'on':
        experts = experts.filter(verification_status='verified')
    
    if search_query:
        experts = experts.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )
    
    # Order by rating and verification status
    experts = experts.annotate(
        review_count=Count('reviews')
    ).order_by('-verification_status', '-average_rating', '-review_count')
    
    # Pagination
    paginator = Paginator(experts, 12)
    page = request.GET.get('page')
    experts_page = paginator.get_page(page)
    
    context = {
        'experts': experts_page,
        'specializations': ExpertProfile.SPECIALIZATION_CHOICES,
        'current_specialization': specialization,
        'current_location': location,
        'verified_only': verified_only,
        'search_query': search_query,
    }
    
    return render(request, 'farmer/browse_experts.html', context)


@login_required
def request_consultation(request, expert_id):
    """Request consultation with an expert"""
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Only farmers can request consultations.")
        return redirect("farmer:login")
    
    from expert.models import ConsultationSession
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
            return redirect("farmer:browse_experts")
        else:
            messages.error(request, "Please fill all required fields.")
    
    context = {
        "expert": expert,
        "session_types": ConsultationSession.SESSION_TYPE,
    }
    
    return render(request, "farmer/request_consultation.html", context)


@login_required
def expert_advice_list(request):
    """View all expert advice received by farmer"""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")
    
    advices = ExpertAdvice.objects.filter(farmer=farmer).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(advices, 10)
    page = request.GET.get('page')
    advices_page = paginator.get_page(page)
    
    context = {
        'advices': advices_page,
    }
    
    return render(request, "farmer/expert_advice.html", context)


@login_required
def expert_advice_detail(request, advice_id):
    """View detailed expert advice"""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")
    
    advice = get_object_or_404(ExpertAdvice, id=advice_id, farmer=farmer)
    
    context = {
        "advice": advice,
    }
    
    return render(request, "farmer/expert_advice_detail.html", context)


@login_required
def sell_to_supplier(request, supplier_id):
    """Allow farmers to sell products to a specific supplier"""
    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
    
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Only farmers can sell to suppliers.")
        return redirect("farmer:login")
        
    # Get farmer's available products that have quantity > 0
    available_products = Product.objects.filter(farmer=farmer, quantity__gt=0)
    
    if not available_products.exists():
        messages.warning(request, "You have no products available to sell. Please add products to your dashboard first.")
        return redirect("supplier:marketplace")

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        total_price = request.POST.get("total_price") # typically calculated on frontend or backend
        
        if product_id and quantity and total_price:
            try:
                quantity = int(quantity)
                product = get_object_or_404(Product, id=product_id, farmer=farmer)
                
                if quantity <= 0:
                    messages.error(request, "Quantity must be greater than zero.")
                elif quantity > product.quantity:
                    messages.error(request, f"You only have {product.quantity} units of {product.name} available.")
                else:
                    from supplier.models import SupplierPurchaseOrder
                    
                    # Create the purchase order request
                    offer = SupplierPurchaseOrder.objects.create(
                        farmer=farmer,
                        supplier=supplier,
                        product=product,
                        quantity=quantity,
                        total_price=float(total_price)
                    )
                    
                    messages.success(request, f"Offer to sell {quantity}x {product.name} sent to {supplier.business_name} successfully!")
                    return redirect("supplier:marketplace")
            except ValueError:
                messages.error(request, "Invalid input. Quantity must be a number.")
        else:
            messages.error(request, "Please fill in all fields.")

    context = {
        "supplier": supplier,
        "available_products": available_products
    }
    
    return render(request, "farmer/sell_to_supplier.html", context)


@login_required
def farmer_marketplace_listings(request):
    """Farmer views their own listings and sees bids sorted highest to lowest."""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")

    from .models import MarketplaceListing
    listings = (
        MarketplaceListing.objects
        .filter(farmer=farmer)
        .prefetch_related('bids__supplier')
        .order_by('-created_at')
    )

    # Attach sorted bids to each listing
    for listing in listings:
        listing.sorted_bids = listing.bids.order_by('-bid_amount')

    context = {
        "farmer": farmer,
        "listings": listings,
    }
    return render(request, "farmer/marketplace_listings.html", context)


@login_required
def create_marketplace_listing(request):
    """Farmer creates a new product listing for open bidding."""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")

    from .models import MarketplaceListing
    available_products = Product.objects.filter(farmer=farmer, quantity__gt=0)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        min_price = request.POST.get("min_price")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit", "kg").strip() or "kg"
        description = request.POST.get("description", "").strip()
        deadline = request.POST.get("deadline")

        if product_id and min_price and quantity and deadline:
            try:
                product = get_object_or_404(Product, id=product_id, farmer=farmer)
                qty = int(quantity)
                if qty <= 0 or qty > product.quantity:
                    messages.error(request, f"Quantity must be between 1 and {product.quantity}.")
                else:
                    from django.utils.dateparse import parse_datetime
                    deadline_dt = parse_datetime(deadline)
                    if not deadline_dt:
                        messages.error(request, "Invalid deadline date/time.")
                    else:
                        from django.utils import timezone as tz
                        from django.conf import settings
                        import pytz
                        if deadline_dt.tzinfo is None:
                            deadline_dt = pytz.timezone(settings.TIME_ZONE).localize(deadline_dt)
                        MarketplaceListing.objects.create(
                            farmer=farmer,
                            product=product,
                            min_price=float(min_price),
                            quantity=qty,
                            unit=unit,
                            description=description,
                            deadline=deadline_dt,
                        )
                        messages.success(request, f"'{product.name}' listed for bidding successfully!")
                        return redirect("farmer:marketplace_listings")
            except (ValueError, Exception) as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Please fill in all required fields.")

    context = {
        "farmer": farmer,
        "available_products": available_products,
    }
    return render(request, "farmer/create_listing.html", context)


@login_required
def accept_bid(request, bid_id):
    """Farmer accepts a specific bid — rejects all others for that listing."""
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Please login as a farmer.")
        return redirect("farmer:login")

    if request.method != "POST":
        return redirect("farmer:marketplace_listings")

    from supplier.models import SupplierBid
    bid = get_object_or_404(SupplierBid, id=bid_id, listing__farmer=farmer)
    listing = bid.listing

    if not listing.is_open:
        messages.error(request, "This listing is no longer open for bids.")
        return redirect("farmer:marketplace_listings")

    # Accept this bid
    bid.status = SupplierBid.STATUS_ACCEPTED
    bid.save()

    # Reject all other bids
    listing.bids.exclude(id=bid.id).update(status=SupplierBid.STATUS_REJECTED)

    # Mark listing as sold
    listing.status = listing.STATUS_SOLD
    listing.save()

    messages.success(
        request,
        f"Bid from {bid.supplier.business_name} (₹{bid.bid_amount}/unit) accepted! They will now proceed to payment."
    )
    return redirect("farmer:marketplace_listings")
