from django.urls import path
from . import views

app_name = "consumer"

urlpatterns = [
    path("consumer/register/", views.consumer_register, name="register"),
    path("consumer/dashboard/", views.consumer_dashboard, name="dashboard"),
    path("consumer/cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("consumer/cart/", views.view_cart, name="view_cart"),
    path("consumer/cart/checkout/", views.checkout, name="checkout"),
    path("consumer/cart/process-payment/", views.process_payment, name="process_payment"),
]
