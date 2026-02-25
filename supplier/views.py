from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Avg, Count

from farmer.models import FarmerProfile
from .models import (
    SupplierProfile, SupplierProduct, SupplyOrder, OrderItem, 
    SupplierReview, SupplierAvailability, SupplierServiceArea,
    SupplierPurchaseOrder
)
from .forms import (
    CustomUserCreationForm, SupplierRegistrationForm, SupplierProductForm,
    SupplierProfileUpdateForm, SupplyOrderForm, SupplierServiceAreaForm
)


def supplier_register(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        supplier_form = SupplierRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and supplier_form.is_valid():
            try:
                user = user_form.save()
                supplier_profile = supplier_form.save(commit=False)
                supplier_profile.user = user
                supplier_profile.save()
                
                login(request, user)
                messages.success(request, "Supplier registration successful! Please login to continue.")
                return redirect("farmer:login")
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
            
            for field, errors in supplier_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        user_form = CustomUserCreationForm()
        supplier_form = SupplierRegistrationForm()
    
    return render(request, "supplier/register.html", {
        "user_form": user_form,
        "supplier_form": supplier_form,
        "business_type_choices": SupplierProfile.BUSINESS_TYPE,
        "certification_choices": SupplierProfile.CERTIFICATION_CHOICES,
    })


@login_required
def supplier_dashboard(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    # Get supplier's products
    products = SupplierProduct.objects.filter(supplier=supplier).order_by('-created_at')
    
    # Get recent orders
    recent_orders = SupplyOrder.objects.filter(supplier=supplier).order_by('-created_at')[:10]
    
    # Get statistics
    total_products = SupplierProduct.objects.filter(supplier=supplier).count()
    total_orders = SupplyOrder.objects.filter(supplier=supplier).count()
    pending_orders = SupplyOrder.objects.filter(supplier=supplier, status='pending').count()
    completed_orders = SupplyOrder.objects.filter(supplier=supplier, status='delivered').count()
    
    # Incoming purchase orders from farmers
    incoming_orders_count = SupplierPurchaseOrder.objects.filter(supplier=supplier, status='pending').count()
    recent_incoming_orders = SupplierPurchaseOrder.objects.filter(supplier=supplier).order_by('-created_at')[:5]
    
    context = {
        "supplier": supplier,
        "products": products[:5],  # Show latest 5 products
        "recent_orders": recent_orders,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "pending_count": pending_orders,
        "incoming_orders_count": incoming_orders_count,
        "recent_incoming_orders": recent_incoming_orders,
    }
    
    return render(request, "supplier/dashboard.html", context)


@login_required
def supplier_profile(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    if request.method == "POST":
        form = SupplierProfileUpdateForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("supplier:profile")
    else:
        form = SupplierProfileUpdateForm(instance=supplier)
    
    # Get service areas
    service_areas = SupplierServiceArea.objects.filter(supplier=supplier)
    
    # Get reviews
    reviews = SupplierReview.objects.filter(supplier=supplier).order_by('-created_at')[:5]
    
    context = {
        "supplier": supplier,
        "form": form,
        "service_areas": service_areas,
        "reviews": reviews,
    }
    
    return render(request, "supplier/profile.html", context)


@login_required
def product_list(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    products = SupplierProduct.objects.filter(supplier=supplier).order_by('-created_at')
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "supplier": supplier,
        "products": page_obj,
        "category_choices": SupplierProduct.PRODUCT_CATEGORY,
        "current_category": category_filter,
        "search_query": search_query,
    }
    
    return render(request, "supplier/products.html", context)


@login_required
def add_product(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    if request.method == "POST":
        form = SupplierProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect("supplier:products")
    else:
        form = SupplierProductForm()
    
    return render(request, "supplier/add_product.html", {
        "form": form,
        "category_choices": SupplierProduct.PRODUCT_CATEGORY,
        "availability_choices": SupplierProduct.AVAILABILITY_STATUS,
    })


@login_required
def edit_product(request, product_id):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    product = get_object_or_404(SupplierProduct, id=product_id, supplier=supplier)
    
    if request.method == "POST":
        form = SupplierProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("supplier:products")
    else:
        form = SupplierProductForm(instance=product)
    
    return render(request, "supplier/edit_product.html", {
        "form": form,
        "product": product,
        "category_choices": SupplierProduct.PRODUCT_CATEGORY,
        "availability_choices": SupplierProduct.AVAILABILITY_STATUS,
    })


@login_required
def orders_list(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    orders = SupplyOrder.objects.filter(supplier=supplier).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "supplier": supplier,
        "orders": page_obj,
        "status_choices": SupplyOrder.ORDER_STATUS,
        "current_status": status_filter,
    }
    
    return render(request, "supplier/orders.html", context)


@login_required
def order_detail(request, order_id):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    order = get_object_or_404(SupplyOrder, id=order_id, supplier=supplier)
    order_items = order.items.all()
    
    if request.method == "POST":
        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            messages.success(request, "Order confirmed successfully!")
            return redirect("supplier:order_detail", order_id=order.id)
    
    context = {
        "order": order,
        "order_items": order_items,
    }
    
    return render(request, "supplier/order_detail.html", context)


@login_required
def update_order_status(request, order_id):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    order = get_object_or_404(SupplyOrder, id=order_id, supplier=supplier)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number', '')
        
        if new_status in [choice[0] for choice in SupplyOrder.ORDER_STATUS]:
            order.status = new_status
            if tracking_number:
                order.tracking_number = tracking_number
            if new_status == 'shipped':
                order.actual_delivery_date = None  # Will be set when delivered
            order.save()
            messages.success(request, f"Order status updated to {order.get_status_display()}")
        else:
            messages.error(request, "Invalid status update.")
    
    return redirect("supplier:order_detail", order_id=order.id)


@login_required
def service_areas(request):
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    service_areas = SupplierServiceArea.objects.filter(supplier=supplier)
    
    if request.method == "POST":
        form = SupplierServiceAreaForm(request.POST)
        if form.is_valid():
            service_area = form.save(commit=False)
            service_area.supplier = supplier
            service_area.save()
            messages.success(request, "Service area added successfully!")
            return redirect("supplier:service_areas")
    else:
        form = SupplierServiceAreaForm()
    
    context = {
        "supplier": supplier,
        "service_areas": service_areas,
        "form": form,
    }
    
    return render(request, "supplier/service_areas.html", context)


@login_required
def marketplace(request):
    # Show all suppliers and products for farmers to browse
    suppliers = SupplierProfile.objects.filter(is_active=True, is_verified=True)
    
    # Filter by business type
    business_type_filter = request.GET.get('business_type')
    if business_type_filter:
        suppliers = suppliers.filter(business_type=business_type_filter)
    
    # Filter by location
    location_filter = request.GET.get('location')
    if location_filter:
        suppliers = suppliers.filter(location__icontains=location_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        suppliers = suppliers.filter(
            Q(business_name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Get products from these suppliers
    products = SupplierProduct.objects.filter(
        supplier__in=suppliers,
        availability_status='in_stock'
    ).order_by('-is_featured', '-created_at')
    
    # Pagination for suppliers
    supplier_paginator = Paginator(suppliers, 12)
    supplier_page = supplier_paginator.get_page(request.GET.get('supplier_page'))
    
    # Pagination for products
    product_paginator = Paginator(products, 24)
    product_page = product_paginator.get_page(request.GET.get('product_page'))
    
    context = {
        "suppliers": supplier_page,
        "products": product_page,
        "business_type_choices": SupplierProfile.BUSINESS_TYPE,
        "current_business_type": business_type_filter,
        "location_filter": location_filter,
        "search_query": search_query,
    }
    
    return render(request, "supplier/marketplace.html", context)


@login_required
def supplier_reviews(request):
    """Show supplier reviews and allow farmers to add reviews"""
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
    
    # Get all reviews for this supplier
    reviews = SupplierReview.objects.filter(supplier=supplier).order_by('-created_at')
    
    # Calculate rating statistics
    total_reviews = reviews.count()
    if total_reviews > 0:
        average_rating = sum(review.rating for review in reviews) / total_reviews
        rating_distribution = {
            5: reviews.filter(rating=5).count(),
            4: reviews.filter(rating=4).count(),
            3: reviews.filter(rating=3).count(),
            2: reviews.filter(rating=2).count(),
            1: reviews.filter(rating=1).count(),
        }
    else:
        average_rating = 0
        rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    
    context = {
        "supplier": supplier,
        "reviews": reviews,
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "rating_distribution": rating_distribution,
    }
    
    return render(request, "supplier/reviews.html", context)


@login_required
def add_supplier_review(request, supplier_id):
    """Allow farmers to add reviews for suppliers"""
    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
    
    try:
        farmer = request.user.farmer_profile
    except AttributeError:
        messages.error(request, "Only farmers can add reviews.")
        return redirect("farmer:login")
    
    # Check if farmer has ordered from this supplier
    has_ordered = SupplyOrder.objects.filter(supplier=supplier, farmer=farmer).exists()
    if not has_ordered:
        messages.error(request, "You can only review suppliers you've ordered from.")
        return redirect("supplier:marketplace")
    
    # Check if review already exists
    existing_review = SupplierReview.objects.filter(farmer=farmer, supplier=supplier).first()
    if existing_review:
        messages.error(request, "You have already reviewed this supplier.")
        return redirect("supplier:marketplace")
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '').strip()
        would_recommend = request.POST.get('would_recommend') == 'on'
        
        if rating and review_text:
            review = SupplierReview.objects.create(
                farmer=farmer,
                supplier=supplier,
                rating=int(rating),
                review_text=review_text,
                would_recommend=would_recommend
            )
            
            # Update supplier's average rating
            supplier.update_rating()
            
            messages.success(request, "Review submitted successfully!")
            return redirect("supplier:marketplace")
        else:
            messages.error(request, "Please provide both rating and review text.")
    
    context = {
        "supplier": supplier,
    }
    
@login_required
def incoming_purchase_orders(request):
    """View all incoming purchase offers from farmers"""
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
        
    orders = SupplierPurchaseOrder.objects.filter(supplier=supplier).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "supplier": supplier,
        "orders": page_obj,
        "status_choices": SupplierPurchaseOrder.ORDER_STATUS,
        "current_status": status_filter,
    }
    
    return render(request, "supplier/incoming_orders.html", context)


@login_required
def respond_purchase_order(request, order_id):
    """Accept or reject an incoming farmer offer"""
    try:
        supplier = request.user.supplier_profile
    except AttributeError:
        messages.error(request, "Please login as a supplier.")
        return redirect("farmer:login")
        
    order = get_object_or_404(SupplierPurchaseOrder, id=order_id, supplier=supplier)
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'accept':
            if order.product.quantity >= order.quantity:
                order.status = 'accepted'
                # Deduct inventory from farmer
                order.product.quantity -= order.quantity
                order.product.save()
                order.save()
                messages.success(request, f"Offer from {order.farmer.user.username} accepted successfully!")
            else:
                messages.error(request, f"Cannot accept offer. The farmer only has {order.product.quantity} units left.")
        elif action == 'reject':
            order.status = 'rejected'
            order.save()
            messages.success(request, "Offer rejected.")
        else:
            messages.error(request, "Invalid action.")
            
    return redirect("supplier:incoming_purchase_orders")
