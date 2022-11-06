from django.urls import path
from django.views.generic import TemplateView

from .views import (
    EventListView,
    EventItemsListView,
    ItemDetailView,
    OrderSummaryView,
    CheckoutView,
    ThankYouView,
    ShopView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="events"),
    path("events/<str:slug>", EventItemsListView.as_view(), name="event_items"),
    path("items", ItemDetailView.as_view(), name="items"),
    path("items/<str:slug>", ItemDetailView.as_view(), name="item_details"),
    path("add-to-cart/<str:slug>", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>", remove_from_cart, name="remove-from-cart"),
    path(
        "remove-single-item-from-cart/<slug>",
        remove_single_item_from_cart,
        name="remove-single-item-from-cart",
    ),
    path("order-summary", OrderSummaryView.as_view(), name="order-summary"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("thanks", ThankYouView.as_view(), name="thanks"),
    path("about", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("shop", ShopView.as_view(), name="shop"),
    path(
        "contact",
        TemplateView.as_view(template_name="core/contact.html"),
        name="contact",
    ),
]
