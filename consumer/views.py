from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from django.shortcuts import redirect, render, get_object_or_404

from farmer.models import MarketOrder, Product
from supplier.models import SupplierProduct
from .models import ConsumerProfile, Cart, CartItem


def consumer_register(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		address = request.POST.get("address", "").strip()
		if form.is_valid():
			user = form.save(commit=False)
			user.role = 'consumer'
			user.save()
			ConsumerProfile.objects.create(user=user, address=address)
			login(request, user)
			return redirect("consumer:dashboard")
	else:
		form = CustomUserCreationForm()
	return render(request, "consumer/register.html", {"form": form})


@login_required
def consumer_dashboard(request):
	user = request.user
	if not hasattr(user, "consumer_profile"):
		messages.error(request, "Please login as a consumer.")
		return redirect("farmer:login")

	consumer = user.consumer_profile

	supplier_products = SupplierProduct.objects.filter(
		availability_status='in_stock', stock_quantity__gt=0
	).select_related('supplier').order_by("-created_at")[:40]
	orders = MarketOrder.objects.filter(consumer=consumer, supplier__isnull=False).order_by("-created_at")

	cart, _ = Cart.objects.get_or_create(consumer=consumer)
	cart_item_count = cart.items.count()

	return render(
		request,
		"consumer/dashboard.html",
		{
			"consumer": consumer,
			"supplier_products": supplier_products,
			"orders": orders,
			"cart_item_count": cart_item_count
		},
	)


@login_required
def add_to_cart(request, product_id):
	if request.method == "POST":
		user = request.user
		if not hasattr(user, "consumer_profile"):
			return redirect("farmer:login")

		consumer = user.consumer_profile
		product = get_object_or_404(Product, id=product_id)
		quantity = int(request.POST.get("quantity", 1))

		if product.quantity < quantity:
			messages.error(request, f"Cannot add. Only {product.quantity} left in stock.")
			return redirect("consumer:dashboard")

		cart, _ = Cart.objects.get_or_create(consumer=consumer)
		cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, supplier_product=None)

		if not created:
			if cart_item.quantity + quantity > product.quantity:
				messages.error(request, f"Cannot add. You already have {cart_item.quantity} in cart, and only {product.quantity} total stock is available.")
				return redirect("consumer:dashboard")
			cart_item.quantity += quantity
			cart_item.save()
		else:
			cart_item.quantity = quantity
			cart_item.save()

		messages.success(request, f"Added {product.name} to cart.")
	return redirect("consumer:dashboard")


@login_required
def add_supplier_to_cart(request, product_id):
	if request.method == "POST":
		user = request.user
		if not hasattr(user, "consumer_profile"):
			return redirect("farmer:login")

		consumer = user.consumer_profile
		sp = get_object_or_404(SupplierProduct, id=product_id, availability_status='in_stock')
		quantity = int(request.POST.get("quantity", 1))

		if sp.stock_quantity < quantity:
			messages.error(request, f"Only {sp.stock_quantity} {sp.unit} available.")
			return redirect("consumer:dashboard")

		cart, _ = Cart.objects.get_or_create(consumer=consumer)
		cart_item, created = CartItem.objects.get_or_create(cart=cart, supplier_product=sp, product=None)

		if not created:
			new_qty = cart_item.quantity + quantity
			if new_qty > sp.stock_quantity:
				messages.error(request, f"Cannot add. You already have {cart_item.quantity} in cart.")
				return redirect("consumer:dashboard")
			cart_item.quantity = new_qty
			cart_item.save()
		else:
			cart_item.quantity = quantity
			cart_item.save()

		messages.success(request, f"Added {sp.name} to cart.")
	return redirect("consumer:dashboard")


@login_required
def view_cart(request):
	user = request.user
	if not hasattr(user, "consumer_profile"):
		return redirect("farmer:login")

	consumer = user.consumer_profile
	cart, _ = Cart.objects.get_or_create(consumer=consumer)
	return render(request, "consumer/cart.html", {"cart": cart})


@login_required
def checkout(request):
	user = request.user
	if not hasattr(user, "consumer_profile"):
		return redirect("farmer:login")

	consumer = user.consumer_profile
	cart, _ = Cart.objects.get_or_create(consumer=consumer)
	if not cart.items.exists():
		messages.error(request, "Your cart is empty.")
		return redirect("consumer:view_cart")

	return render(request, "consumer/checkout.html", {"cart": cart})


@login_required
def process_payment(request):
	user = request.user
	if not hasattr(user, "consumer_profile"):
		return redirect("farmer:login")

	if request.method == "POST":
		consumer = user.consumer_profile
		cart = getattr(consumer, "cart", None)
		if not cart or not cart.items.exists():
			messages.error(request, "Cart is empty.")
			return redirect("consumer:dashboard")

		# Pre-flight stock check
		for item in cart.items.all():
			if item.product:
				if item.product.quantity < item.quantity:
					messages.error(request, f"Sorry, {item.product.name} only has {item.product.quantity} items left. Please update your cart.")
					return redirect("consumer:view_cart")
			elif item.supplier_product:
				if item.supplier_product.stock_quantity < item.quantity:
					messages.error(request, f"Sorry, {item.supplier_product.name} only has {item.supplier_product.stock_quantity} {item.supplier_product.unit} left. Please update your cart.")
					return redirect("consumer:view_cart")

		for item in cart.items.all():
			if item.product:
				MarketOrder.objects.create(
					farmer=item.product.farmer,
					consumer=consumer,
					product=item.product,
					quantity=item.quantity,
					status=MarketOrder.STATUS_PENDING
				)
				# Deduct quantity from original product model so farmer sees it go down
				item.product.quantity -= item.quantity
				item.product.save(update_fields=['quantity'])
			elif item.supplier_product:
				MarketOrder.objects.create(
					supplier=item.supplier_product.supplier,
					consumer=consumer,
					supplier_product=item.supplier_product,
					quantity=item.quantity,
					status=MarketOrder.STATUS_PENDING
				)
				# Deduct quantity from supplier product
				item.supplier_product.stock_quantity -= item.quantity
				item.supplier_product.save(update_fields=['stock_quantity'])

		cart.items.all().delete()
		messages.success(request, "Payment successful! Your orders have been placed.")
		return redirect("consumer:dashboard")

	return redirect("consumer:checkout")
