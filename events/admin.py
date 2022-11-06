from django.contrib import admin

from .models import Address, Coupon, EventType, Item, Order, OrderItem

admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)


class EventTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Item, ItemAdmin)
