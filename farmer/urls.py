from django.urls import path
from . import views

app_name = "farmer"

urlpatterns = [
	path("", views.home, name="home"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("farmer/register/", views.farmer_register, name="register"),
	path("farmer/dashboard/", views.farmer_dashboard, name="dashboard"),
	path("experts/", views.browse_experts, name="browse_experts"),
	path("expert/<int:expert_id>/request/", views.request_consultation, name="request_consultation"),
	path("expert-advice/", views.expert_advice_list, name="expert_advice"),
	path("expert-advice/<int:advice_id>/", views.expert_advice_detail, name="expert_advice_detail"),
	path("sell-to-supplier/<int:supplier_id>/", views.sell_to_supplier, name="sell_to_supplier"),
	# Marketplace Bidding
	path("farmer/marketplace/", views.farmer_marketplace_listings, name="marketplace_listings"),
	path("farmer/marketplace/create/", views.create_marketplace_listing, name="create_marketplace_listing"),
	path("farmer/marketplace/bid/<int:bid_id>/accept/", views.accept_bid, name="accept_bid"),
]


