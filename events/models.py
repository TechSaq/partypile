from django.db import models
from django.shortcuts import reverse  # type: ignore
from django.conf import settings


class EventType(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="event_type")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event_items", kwargs={"slug": self.slug})


class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    event_types = models.ManyToManyField(EventType)
    image = models.ImageField(upload_to="items")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:item_details", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("events:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("events:remove-from-cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        "Address",
        related_name="address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.CASCADE, blank=True, null=True
    )
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_cart_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"


class Coupon(models.Model):
    code = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code
