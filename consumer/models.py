from django.db import models
from django.conf import settings
from farmer.models import Product
from supplier.models import SupplierProduct


class ConsumerProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer_profile")
	address = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.user.username


class Cart(models.Model):
    consumer = models.OneToOneField(ConsumerProfile, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart({self.consumer.user.username})"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        name = self.supplier_product.name if self.supplier_product else (self.product.name if self.product else "?")
        return f"{self.quantity} x {name}"

    @property
    def item_name(self):
        if self.supplier_product:
            return self.supplier_product.name
        return self.product.name if self.product else ""

    @property
    def item_price(self):
        if self.supplier_product:
            return self.supplier_product.price
        return self.product.price if self.product else 0

    @property
    def total_price(self):
        return self.item_price * self.quantity
