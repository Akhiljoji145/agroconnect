from django.contrib import admin
from .models import (
    SupplierProfile, SupplierProduct, SupplyOrder, OrderItem,
    SupplierReview, SupplierAvailability, SupplierServiceArea
)


@admin.register(SupplierProfile)
class SupplierProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_type', 'location', 'is_verified', 'is_active', 'created_at']
    list_filter = ['business_type', 'is_verified', 'is_active', 'created_at']
    search_fields = ['business_name', 'location', 'description']
    readonly_fields = ['total_products', 'total_orders', 'average_rating']


@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'category', 'price', 'availability_status', 'is_featured', 'created_at']
    list_filter = ['category', 'availability_status', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'supplier__business_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SupplyOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'farmer', 'supplier', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'farmer__user__username', 'supplier__business_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['product__name', 'order__order_id']


@admin.register(SupplierReview)
class SupplierReviewAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'supplier', 'rating', 'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = ['farmer__user__username', 'supplier__business_name', 'review_text']


@admin.register(SupplierAvailability)
class SupplierAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'day_of_week', 'opening_time', 'closing_time', 'is_closed']
    list_filter = ['day_of_week', 'is_closed']
    search_fields = ['supplier__business_name']


@admin.register(SupplierServiceArea)
class SupplierServiceAreaAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'district', 'taluk', 'delivery_charge', 'min_order_amount']
    list_filter = ['district']
    search_fields = ['supplier__business_name', 'district', 'taluk', 'villages']
