from django.urls import path
from . import views

app_name = "supplier"

urlpatterns = [
    path("supplier/register/", views.supplier_register, name="register"),
    path("supplier/dashboard/", views.supplier_dashboard, name="dashboard"),
    path("supplier/profile/", views.supplier_profile, name="profile"),
    path("supplier/products/", views.product_list, name="products"),
    path("supplier/products/add/", views.add_product, name="add_product"),
    path("supplier/products/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("supplier/orders/", views.orders_list, name="orders"),
    path("supplier/orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("supplier/orders/<int:order_id>/update/", views.update_order_status, name="update_order_status"),
    path("supplier/service-areas/", views.service_areas, name="service_areas"),
    path("supplier/reviews/", views.supplier_reviews, name="reviews"),
    path("supplier/<int:supplier_id>/review/", views.add_supplier_review, name="add_review"),
    path("marketplace/", views.marketplace, name="marketplace"),
    path("supplier/incoming-orders/", views.incoming_purchase_orders, name="incoming_purchase_orders"),
    path("supplier/incoming-orders/<int:order_id>/respond/", views.respond_purchase_order, name="respond_purchase_order"),
    # Farmer Marketplace Bidding
    path("supplier/farmer-market/", views.supplier_farmer_marketplace, name="farmer_marketplace"),
    path("supplier/farmer-market/<int:listing_id>/bid/", views.place_bid, name="place_bid"),
    path("supplier/my-bids/", views.supplier_my_bids, name="my_bids"),
    path("supplier/market-orders/<int:order_id>/accept/", views.accept_market_order, name="accept_market_order"),
]

