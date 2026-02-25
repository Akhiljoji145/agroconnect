from django.db import models
from django.contrib.auth.models import User


class FarmerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farmer_profile")
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


class MarketOrder(models.Model):
	STATUS_PENDING = "pending"
	STATUS_CONFIRMED = "confirmed"
	STATUS_SHIPPED = "shipped"
	STATUS_DELIVERED = "delivered"

	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_CONFIRMED, "Confirmed"),
		(STATUS_SHIPPED, "Shipped"),
		(STATUS_DELIVERED, "Delivered"),
	]

	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="orders")
	consumer = models.ForeignKey("consumer.ConsumerProfile", on_delete=models.SET_NULL, null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Order({self.id}, {self.status})"


class FarmerChatMessage(models.Model):
	farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="chat_messages")
	message = models.TextField(blank=True)
	document = models.FileField(upload_to="chat_documents/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Message by {self.farmer} at {self.created_at}"
