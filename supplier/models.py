from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class SupplierProfile(models.Model):
    BUSINESS_TYPE = [
        ('seeds', 'Seeds & Planting Material'),
        ('fertilizers', 'Fertilizers & Nutrients'),
        ('pesticides', 'Pesticides & Crop Protection'),
        ('machinery', 'Farm Machinery & Equipment'),
        ('irrigation', 'Irrigation Systems'),
        ('organic', 'Organic Farming Supplies'),
        ('livestock', 'Livestock Feed & Medicine'),
        ('storage', 'Storage & Processing'),
    ]
    
    CERTIFICATION_CHOICES = [
        ('organic', 'Organic Certified'),
        ('iso', 'ISO Certified'),
        ('government', 'Government Approved'),
        ('local', 'Locally Verified'),
        ('none', 'Not Certified'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supplier_profile")
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPE)
    description = models.TextField(help_text="Describe your business and specialties")
    location = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2024)])
    certifications = models.CharField(max_length=20, choices=CERTIFICATION_CHOICES, default='none')
    certification_documents = models.FileField(upload_to="supplier_documents/", blank=True, null=True)
    business_license = models.FileField(upload_to="supplier_documents/", blank=True, null=True)
    logo = models.ImageField(upload_to="supplier_logos/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} - {self.get_business_type_display()}"

    def update_rating(self):
        reviews = SupplierReview.objects.filter(supplier=self)
        if reviews:
            self.average_rating = sum(review.rating for review in reviews) / len(reviews)
        else:
            self.average_rating = 0
        self.save()


class SupplierProduct(models.Model):
    PRODUCT_CATEGORY = [
        ('seeds', 'Seeds'),
        ('fertilizers', 'Fertilizers'),
        ('pesticides', 'Pesticides'),
        ('machinery', 'Machinery'),
        ('irrigation', 'Irrigation'),
        ('organic', 'Organic Products'),
        ('livestock', 'Livestock'),
        ('tools', 'Farming Tools'),
    ]
    
    AVAILABILITY_STATUS = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('limited', 'Limited Stock'),
        ('pre_order', 'Pre-Order'),
    ]
    
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=PRODUCT_CATEGORY)
    description = models.TextField(help_text="Detailed product description")
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=50, help_text="e.g., kg, liters, pieces, bags")
    min_order_quantity = models.PositiveIntegerField(default=1)
    max_order_quantity = models.PositiveIntegerField(default=1000)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='in_stock')
    stock_quantity = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to="supplier_products/", blank=True, null=True)
    specifications = models.JSONField(default=dict, blank=True, help_text="Product specifications as JSON")
    is_featured = models.BooleanField(default=False)
    is_organic = models.BooleanField(default=False)
    delivery_time_days = models.PositiveIntegerField(default=7, help_text="Estimated delivery time in days")
    return_policy = models.TextField(blank=True, help_text="Return and exchange policy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.supplier.business_name}"

    @property
    def is_available(self):
        return self.availability_status == 'in_stock' and self.stock_quantity > 0


class SupplyOrder(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Payment Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Payment Failed'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True)
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, related_name="supply_orders")
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    delivery_address = models.TextField()
    delivery_notes = models.TextField(blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.farmer.user.username}"

    @property
    def is_delivered(self):
        return self.status == 'delivered'


class OrderItem(models.Model):
    order = models.ForeignKey(SupplyOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class SupplierPurchaseOrder(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, related_name="sales_to_suppliers")
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="incoming_purchase_orders")
    
    # We reference the farmer's Product that they are trying to sell
    product = models.ForeignKey('farmer.Product', on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer from {self.farmer.user.username} to {self.supplier.business_name}: {self.product.name}"



class SupplierReview(models.Model):
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, related_name="supplier_reviews")
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="reviews")
    order = models.ForeignKey(SupplyOrder, on_delete=models.CASCADE, related_name="review", null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(max_length=1000)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['farmer', 'supplier']

    def __str__(self):
        return f"Review: {self.farmer.user.username} - {self.supplier.business_name} ({self.rating}/5)"


class SupplierAvailability(models.Model):
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="availability_schedule")
    day_of_week = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)
    special_notes = models.TextField(blank=True, help_text="Special hours or holiday notes")

    class Meta:
        unique_together = ['supplier', 'day_of_week']

    def __str__(self):
        return f"{self.supplier.business_name} - Day {self.day_of_week}"


class SupplierServiceArea(models.Model):
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="service_areas")
    district = models.CharField(max_length=100, help_text="Kerala district")
    taluk = models.CharField(max_length=100, blank=True, help_text="Taluk within district")
    villages = models.TextField(blank=True, help_text="List of villages served")
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Delivery charge in rupees")
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Minimum order amount for free delivery")

    def __str__(self):
        return f"{self.supplier.business_name} - {self.district}"


class SupplierBid(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    PAYMENT_UNPAID = 'unpaid'
    PAYMENT_PAID = 'paid'

    PAYMENT_CHOICES = [
        (PAYMENT_UNPAID, 'Unpaid'),
        (PAYMENT_PAID, 'Paid'),
    ]

    listing = models.ForeignKey('farmer.MarketplaceListing', on_delete=models.CASCADE, related_name='bids')
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name='bids_placed')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Offered price per unit (₹)')
    message = models.TextField(blank=True, help_text='Optional message to the farmer')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=PAYMENT_UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['listing', 'supplier']
        ordering = ['-bid_amount']

    def __str__(self):
        return f"Bid by {self.supplier.business_name} on {self.listing} — ₹{self.bid_amount}/unit"
