from django.db import models
from django.conf import settings


class FarmerProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farmer_profile")
	farm_name = models.CharField(max_length=120, blank=True)
	location = models.CharField(max_length=120, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.farm_name or self.user.username


class SoilAnalysis(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="soil_analyses")
	ph = models.DecimalField(max_digits=4, decimal_places=2)
	moisture = models.DecimalField(max_digits=5, decimal_places=2)
	temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	nitrogen = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	phosphorus = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	potassium = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	health_score = models.CharField(max_length=50, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"SoilAnalysis({self.farmer_id}, {self.created_at.date()})"


class FarmerPost(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="posts")
	image = models.ImageField(upload_to="farmer_posts/", blank=True, null=True)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Post({self.farmer_id}, {self.created_at.date()})"


class Product(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="products")
	supplier = models.ForeignKey('supplier.SupplierProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="supplied_products")
	name = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.name


class InventoryItem(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="inventory")
	name = models.CharField(max_length=120)
	quantity = models.PositiveIntegerField(default=0)
	unit = models.CharField(max_length=30, default="unit")
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.name

from supplier.models import SupplierProduct, SupplierProfile

class MarketOrder(models.Model):
	STATUS_PENDING = "pending"
	STATUS_ACCEPTED = "accepted"
	STATUS_CONFIRMED = "confirmed"
	STATUS_SHIPPED = "shipped"
	STATUS_DELIVERED = "delivered"

	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_ACCEPTED, "Accepted"),
		(STATUS_CONFIRMED, "Confirmed"),
		(STATUS_SHIPPED, "Shipped"),
		(STATUS_DELIVERED, "Delivered"),
	]

	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
	supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="consumer_orders", null=True, blank=True)
	consumer = models.ForeignKey("consumer.ConsumerProfile", on_delete=models.SET_NULL, null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Order({self.id}, {self.status})"

	@property
	def total_price(self):
		if self.supplier_product:
			return self.supplier_product.price * self.quantity
		if self.product:
			return self.product.price * self.quantity
		return 0


class FarmerChatMessage(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="chat_messages")
	message = models.TextField(blank=True)
	document = models.FileField(upload_to="chat_documents/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Message by {self.farmer} at {self.created_at}"


class MarketplaceListing(models.Model):
	STATUS_OPEN = 'open'
	STATUS_CLOSED = 'closed'
	STATUS_SOLD = 'sold'

	STATUS_CHOICES = [
		(STATUS_OPEN, 'Open for Bids'),
		(STATUS_CLOSED, 'Closed'),
		(STATUS_SOLD, 'Sold'),
	]

	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='marketplace_listings')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='listings')
	min_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Minimum bid price per unit (₹)')
	quantity = models.PositiveIntegerField(help_text='Quantity available for this listing')
	unit = models.CharField(max_length=30, default='kg', help_text='e.g. kg, bags, tons')
	description = models.TextField(blank=True, help_text='Additional details about this listing')
	deadline = models.DateTimeField(help_text='Auction deadline')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.product.name} ({self.quantity} {self.unit}) by {self.farmer}"

	@property
	def is_open(self):
		from django.utils import timezone
		return self.status == self.STATUS_OPEN and self.deadline > timezone.now()
