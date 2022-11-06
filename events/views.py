from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import EventType, Item, Order, OrderItem


class ItemsListView(ListView):
    model = Item
    context_object_name = "items"
    template_name = "events/items_list.html"


class EventListView(ListView):
    model = EventType
    context_object_name = "event_types"
    template_name = "core/homepage.html"


class EventItemsListView(ListView):
    context_object_name = "items"
    template_name = "events/items_list.html"

    def get_queryset(self):
        self.event_type = get_object_or_404(EventType, slug=self.kwargs["slug"])
        return Item.objects.filter(event_types=self.event_type)


class ItemDetailView(DetailView):
    model = Item
    context_object_name = "item"
    template_name = "events/item_detail.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {"cart": order}
            return render(self.request, "events/order_summary.html", context)
        except ObjectDoesNotExist:
            # messages.warning(self.request, "You don't have any active order!!")
            return redirect("/")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {"cart": order}
        except ObjectDoesNotExist:
            # messages.info(self.request, "Currently you don't have any ordrs")
            return redirect("/")

        return render(self.request, "events/checkout.html", context)


class ShopView(ListView):
    model = Item
    context_object_name = "items"
    template_name = "events/items_list.html"


class ThankYouView(DetailView):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            "events/thanks.html",
        )

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            order.is_ordered = True
            order.save()
        except ObjectDoesNotExist:
            pass

        return render(
            self.request,
            "events/thanks.html",
        )


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, is_ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    print(order_qs)

    if order_qs.exists():
        order = order_qs[0]

        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            print(order_item.quantity)
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, "This item quantity was updated")
            return redirect("events:order-summary")
        else:
            # messages.info(request, "This item is added to your cart")
            order.items.add(order_item)
            return redirect("events:order-summary")
    else:
        print("creating")
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        # messages.info(request, "This item is added to your cart")
        order.items.add(order_item)
        return redirect("events:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, is_ordered=False
            )[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            # messages.info(request, "This item is removed from your cart")
            return redirect("events:order-summary")
        else:
            # messages.info(request, "This item is not in your cart")
            return redirect("events:item_details", slug=slug)
    else:
        # messages.info(request, "You don't have any order yet.")
        return redirect("events:item_details", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, is_ordered=False
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            # messages.info(request, "This item is updated");
            return redirect("events:order-summary")
        else:
            # messages.info(request, "This item is not in your cart");
            return redirect("event:item_details", slug=slug)
    else:
        # messages.info(request, "You don't have any order yet.");
        return redirect("event:item_details", slug=slug)
